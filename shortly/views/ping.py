from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

class Ping(APIView):
    def get(self, request: Request)-> Response:
        return Response({
            "status": "healthy",
            "message": "Pong"
        }, status=status.HTTP_200_OK)

