from django.http import JsonResponse
from django.views import View
from apps.ingestion.models import IngestionData
import psycopg2
import os

class DataView(View):
    def get(self, request):
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

        cursor.execute("SELECT * FROM ingestion_data")
        rows = cursor.fetchall()

        data = IngestionData.objects.all().values('id', 'message')

        return JsonResponse(list(data), safe=False)