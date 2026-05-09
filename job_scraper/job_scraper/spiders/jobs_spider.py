import scrapy
from job_scraper.items import JobItem
from job_scraper.kafka_producer import send_to_kafka

class JobsSpider(scrapy.Spider):
    name = "jobs"
    start_urls = ["https://www.rekrute.com/offres-emploi-maroc.html"]

    def clean(self, text):
        if text:
            return " ".join(text.split())
        return ""

    def parse(self, response):
        jobs = response.css("div.section")

        for job in jobs:
            url = response.urljoin(
                job.css("a.titreJob::attr(href)").get()
            )

            # ignorer liens invalides
            if not url or "offres.html" in url:
                continue

            item = JobItem()

            # 🔹 titre + location
            title_full = self.clean(job.css("a.titreJob::text").get())

            if not title_full:
                continue

            if "|" in title_full:
                title, location = title_full.split("|")
            else:
                title, location = title_full, ""

            item['title'] = title.strip()
            item['location'] = location.strip()
            item['url'] = url

            # 🔹 description
            item['description'] = self.clean(
                job.css("div.info span::text").get()
            )

            # 🔹 date
            item['date'] = self.clean(
                job.css("em.date span::text").get()
            )

            # 🔹 valeurs par défaut
            item['sector'] = "N/A"
            item['function'] = "N/A"
            item['experience'] = "N/A"
            item['education'] = "N/A"
            item['contract'] = "N/A"

            # 🔹 extraction
            for li in job.css("ul li"):
                label = self.clean(" ".join(li.css("::text").getall()))

                if "Secteur" in label:
                    item['sector'] = label.split(":")[-1].strip()

                elif "Fonction" in label:
                    item['function'] = label.split(":")[-1].strip()

                elif "Expérience" in label:
                    item['experience'] = label.split(":")[-1].strip()

                elif "Niveau" in label:
                    item['education'] = label.split(":")[-1].strip()

                elif "Type de contrat" in label:
                    contract = label.replace("Type de contrat proposé :", "").strip()
                    contract = contract.replace(" - ", " | ")
                    contract = contract.replace("| |", "|")
                    item['contract'] = contract

            # 🔥 STREAMING → Kafka
            send_to_kafka(dict(item))
            yield item

        # 🔹 pagination
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)