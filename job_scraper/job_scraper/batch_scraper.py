import time
import subprocess

while True:
    print("Lancement scraping batch...")

    subprocess.run(["scrapy", "crawl", "jobs"])

    print("1 heure...")
    time.sleep(3600)