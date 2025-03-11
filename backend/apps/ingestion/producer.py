from kafka import KafkaProducer
import json

KAFKA_BROKER = "kafka:9092"
TOPIC = "data_ingestion"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_data(data):
    producer.send(TOPIC, data)
    producer.flush()

if __name__ == "__main__":
    test_data = {"id": 1, "message": "Teste de ingestão de dados"}
    send_data(test_data)
    print("Mensagem enviada ao Kafka!")
