from django.contrib import admin
from .models import IngestionData

@admin.register(IngestionData)
class IngestionDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'message')