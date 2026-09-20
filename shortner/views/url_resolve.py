from django.core.cache import cache
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from ..models import URL, url_cache_key

class URLResolve(APIView):
    def get(self, request: Request, short_code: str):
        long_url = cache.get(url_cache_key(short_code))
        if long_url is not None:
            return HttpResponseRedirect(long_url)

        try:
            url = URL.objects.get(short_code = short_code)
        except URL.DoesNotExist:
            return Response({"error": "short_code not found"}, status=status.HTTP_404_NOT_FOUND)

        long_url = url.resolve_url()
        url.cache_long_url()
        return HttpResponseRedirect(long_url)

