from minio import Minio
import pandas as pd
import json
import io
import re

# 🔗 Connexion MinIO
client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

bucket = "jobs"

# =========================
# 📥 LECTURE BRONZE
# =========================

objects = client.list_objects(bucket, prefix="bronze/", recursive=True)

data = []

for obj in objects:
    response = client.get_object(bucket, obj.object_name)
    content = response.read().decode('utf-8')

    try:
        job = json.loads(content)
        data.append(job)
    except:
        print("Erreur fichier:", obj.object_name)

df = pd.DataFrame(data)
print("Bronze count:", len(data))

# =========================
# 🧹 NETTOYAGE
# =========================

df.drop_duplicates(inplace=True)
df.fillna("unknown", inplace=True)

df['source'] = "rekrute"

df['title'] = df['title'].str.strip().str.lower()
df['location'] = df['location'].fillna("unknown").str.strip()
df['description'] = df['description'].str.strip().str.lower()

# supprimer HTML
df['description'] = df['description'].apply(lambda x: re.sub(r'<.*?>', '', x))

# =========================
# 🌍 STRUCTURATION
# =========================

# ville / pays
df[['city', 'country']] = df['location'].str.extract(r'(.+)\s\((.+)\)')

df['city'] = df['city'].fillna("unknown").str.lower().str.strip()

# 🔥 nettoyage sector PRO
df['sector'] = df['sector'].fillna("unknown")
df['sector'] = df['sector'].str.replace(" , ", " - ")
df['sector'] = df['sector'].str.replace(",", " - ")
df['sector'] = df['sector'].str.split(' - ')

df = df.explode('sector')

df['sector'] = df['sector'].str.strip().str.lower()
df = df[df['sector'] != ""]

# =========================
# 🧪 QUALITÉ
# =========================

df = df[df['title'] != ""]
df = df[df['description'].str.len() > 20]

# =========================
# 🌐 LANGUE
# =========================

def detect_lang(text):
    if any(word in text for word in ["le", "la", "des", "une"]):
        return "fr"
    return "unknown"

df['language'] = df['description'].apply(detect_lang)

# =========================
# 🔥 ENRICHISSEMENT
# =========================

def extract_years(exp):
    match = re.search(r'(\d+)', str(exp))
    if match:
        return int(match.group(1))
    return 0

if 'experience' not in df.columns:
    df['experience'] = "unknown"

df['experience_years'] = df['experience'].apply(extract_years)

def categorize_exp(exp):
    exp = str(exp).lower()
    if "débutant" in exp:
        return "junior"
    elif "intermédiaire" in exp:
        return "mid"
    elif "senior" in exp:
        return "senior"
    return "unknown"

df['experience_level'] = df['experience'].apply(categorize_exp)

# =========================
# 💾 SAUVEGARDE
# =========================

clean_json = json.dumps(
    df.to_dict(orient="records"),
    ensure_ascii=False,
    indent=2
).encode("utf-8")

client.put_object(
    bucket,
    "silver/jobs_clean.json",
    data=io.BytesIO(clean_json),
    length=len(clean_json),
    content_type='application/json'
)

print("✅ Silver layer created")
print("After cleaning:", len(df))