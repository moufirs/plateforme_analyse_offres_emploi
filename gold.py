from minio import Minio
import pandas as pd
import json
import io

# 🔗 Connexion MinIO
client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

bucket = "jobs"

# =========================
# 📥 LECTURE SILVER
# =========================

response = client.get_object(bucket, "silver/jobs_clean.json")
data = json.loads(response.read().decode("utf-8"))

df = pd.DataFrame(data)

# =========================
# 🛡️ SÉCURITÉ COLONNES
# =========================

required_cols = ["city", "sector", "title", "date", "url", "experience_level"]

for col in required_cols:
    if col not in df.columns:
        df[col] = "unknown"

# =========================
# 📊 ANALYSE
# =========================

# 📍 jobs par ville
jobs_by_city = df['city'].value_counts().to_dict()

# 🏢 jobs par secteur
jobs_by_sector = df['sector'].value_counts().to_dict()

# 💼 top métiers
top_jobs = df['title'].value_counts().head(10).to_dict()

# 📅 jobs par date
jobs_by_date = df['date'].value_counts().to_dict()

# 📊 total jobs uniques
total_jobs = df['url'].nunique()

# 📊 total lignes (après explode)
total_rows = len(df)

# 📊 expérience
jobs_by_experience = df['experience_level'].value_counts().to_dict()

# 🔥 top villes
top_cities = df['city'].value_counts().head(5).to_dict()

# 🔥 top secteurs
top_sectors = df['sector'].value_counts().head(5).to_dict()

# =========================
# 📦 STRUCTURE
# =========================

gold_data = {
    "total_jobs": total_jobs,
    "total_rows": total_rows,
    "jobs_by_city": jobs_by_city,
    "jobs_by_sector": jobs_by_sector,
    "jobs_by_experience": jobs_by_experience,
    "top_jobs": top_jobs,
    "jobs_by_date": jobs_by_date,
    "top_cities": top_cities,
    "top_sectors": top_sectors
}

# =========================
# 💾 SAUVEGARDE
# =========================

json_data = json.dumps(
    gold_data,
    ensure_ascii=False,
    indent=2
).encode("utf-8")

client.put_object(
    bucket,
    "gold/stats.json",
    data=io.BytesIO(json_data),
    length=len(json_data),
    content_type='application/json'
)

print("✅ Gold layer created")
print("Total jobs:", total_jobs)
print("Total rows:", total_rows)
