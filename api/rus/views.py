from django.http import JsonResponse
from rest_framework.views import APIView


class TestAddView(APIView):

    @staticmethod
    def get(request):
        return JsonResponse({'status': "OK"})
