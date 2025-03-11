from kafka import KafkaConsumer
import json
import psycopg2
import os

KAFKA_BROKER = "kafka:9092"
TOPIC = "data_ingestion"

DB_NAME = os.getenv("POSTGRES_DB", "alakazan_db")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = "db"
DB_PORT = "5432"

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("Iniciando consumer...")
for message in consumer:
    data = message.value
    print(f"Recebido: {data}")


    cursor.execute(
        "INSERT INTO ingestion_data (id, message) VALUES (%s, %s)",
        (data["id"], data["message"])
    )
    conn.commit()
