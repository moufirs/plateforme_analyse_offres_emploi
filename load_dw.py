from minio import Minio
import json
import mysql.connector

# 🔗 Connexion MinIO
client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

bucket = "jobs"

# 📥 lire gold depuis MinIO
response = client.get_object(bucket, "gold/stats.json")
gold_data = json.loads(response.read().decode("utf-8"))

# 🔗 Connexion MySQL
conn = mysql.connector.connect(
    host="mysql",
    user="root",
    password="root123",
    database="job_datawarehouse"
)

cursor = conn.cursor()

# 📊 Jobs par date
cursor.execute("DELETE FROM jobs_by_date")

for date, total in gold_data["jobs_by_date"].items():
    cursor.execute(
        "INSERT INTO jobs_by_date (date, total) VALUES (%s, %s)",
        (date, total)
    )

# 📊 Jobs par secteur
cursor.execute("DELETE FROM jobs_by_sector")

for sector, total in gold_data["jobs_by_sector"].items():
    cursor.execute(
        "INSERT INTO jobs_by_sector (sector, total) VALUES (%s, %s)",
        (sector, total)
    )

# 📊 Jobs par ville
cursor.execute("DELETE FROM jobs_by_city")

for city, total in gold_data["jobs_by_city"].items():
    cursor.execute(
        "INSERT INTO jobs_by_city (city, total) VALUES (%s, %s)",
        (city, total)
    )

conn.commit()
conn.close()

print("✅ Data Warehouse updated")