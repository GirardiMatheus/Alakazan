import logging
from kafka import KafkaConsumer
import json
import psycopg2
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BROKER = "kafka:9092"
TOPIC = "data_ingestion"

DB_NAME = os.getenv("POSTGRES_DB", "alakazan_db")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = "db"
DB_PORT = "5432"

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    logger.info("Conexão com o PostgreSQL estabelecida com sucesso.")
except Exception as e:
    logger.error(f"Erro ao conectar ao PostgreSQL: {e}")
    raise

try:
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")))
    logger.info("Consumer do Kafka configurado com sucesso.")
except Exception as e:
    logger.error(f"Erro ao configurar o consumer do Kafka: {e}")
    raise

logger.info("Iniciando consumer...")
for message in consumer:
    try:
        data = message.value
        logger.info(f"Recebido: {data}")

        cursor.execute(
            "INSERT INTO ingestion_data (id, message) VALUES (%s, %s)",
            (data["id"], data["message"])
        )
        conn.commit()
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        conn.rollback()