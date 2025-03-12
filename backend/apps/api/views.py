from django.http import JsonResponse
from django.views import View
from apps.ingestion.models import IngestionData  

class DataView(View):
    def get(self, request):
        data = IngestionData.objects.all().values('id', 'message')
        return JsonResponse(list(data), safe=False)