from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from ..models import URL

class URLResolve(APIView):
    def get(self, request: Request, short_code: str):
        try:
            url = URL.objects.get(short_code = short_code)
            return HttpResponseRedirect(url.resolve_url())
        except URL.DoesNotExist:
            return Response({"error": "short_code not found"}, status=status.HTTP_404_NOT_FOUND)

