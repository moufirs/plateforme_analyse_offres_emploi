from kafka import KafkaConsumer
from minio import Minio
import json
import io
from datetime import datetime
import uuid
import os

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9092")
MINIO_SERVER = os.getenv("MINIO_SERVER", "localhost:9000")

consumer = KafkaConsumer(
    'jobs_topic',
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)



client = Minio(
    MINIO_SERVER,
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

bucket = "jobs"

if not client.bucket_exists(bucket):
    client.make_bucket(bucket)

for msg in consumer:
    data = msg.value

    # 📅 date actuelle
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    # 🔥 chemin partitionné
    object_name = f"bronze/year={year}/month={month}/day={day}/job_{uuid.uuid4()}.json"

    json_data = json.dumps(data).encode('utf-8')

    client.put_object(
        bucket,
        object_name,
        data=io.BytesIO(json_data),
        length=len(json_data),
        content_type='application/json'
    )

    print("Saved:", object_name)