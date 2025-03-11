from pyspark.sql import SparkSession
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_NAME = os.getenv("POSTGRES_DB", "alakazan_db")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = "db"
DB_PORT = "5432"

spark = SparkSession.builder \
    .appName("AlakazanDataProcessing") \
    .getOrCreate()

logger.info("Spark session initialized successfully.")

try:
    df = spark.read \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}") \
        .option("dbtable", "ingestion_data") \
        .option("user", DB_USER) \
        .option("password", DB_PASS) \
        .load()

    logger.info("Data successfully loaded from PostgreSQL.")

    message_count = df.count()
    logger.info(f"Total messages processed: {message_count}")

    filtered_df = df.filter(df["id"] > 10)
    filtered_count = filtered_df.count()
    logger.info(f"Filtered messages (ID > 10): {filtered_count}")

    filtered_df.write \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}") \
        .option("dbtable", "processed_data") \
        .option("user", DB_USER) \
        .option("password", DB_PASS) \
        .mode("overwrite") \
        .save()

    logger.info("Processed data saved to PostgreSQL.")

except Exception as e:
    logger.error(f"Error during Spark job execution: {e}")
    raise

finally:
    spark.stop()
    logger.info("Spark session stopped.")