# src/core_apps/common/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
def test_view(request):
    response = JsonResponse({'message': 'This is a test view.'})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    response["Access-Control-Allow-Headers"] = "Authorization, Content-Type, X-CSRFToken"
    response["Access-Control-Allow-Credentials"] = "true"
    return response
