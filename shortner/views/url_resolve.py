from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from ..models import URL

class URLResolve(APIView):
    def get(self, request: Request, short_code: str)-> Response:
        url = URL.objects.get(short_code = short_code)
        return Response(url.resolve_url, status=status.HTTP_301_MOVED_PERMANENTLY)

