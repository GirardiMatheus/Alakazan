from django.db import models

class IngestionData(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField()

    def __str__(self):
        return f"ID: {self.id}, Message: {self.message}"