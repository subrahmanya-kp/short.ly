from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from pydantic import BaseModel, ValidationError, HttpUrl
from datetime import datetime
from typing import Optional

from ..models import URL

class URLValidate(BaseModel):
    long_url: HttpUrl
    expiry: Optional[datetime] = None

class URLAdd(APIView):
    def post(self, request: Request)-> Response:
        try:
            payload = URLValidate.model_validate(request.data)
            url, created = URL.objects.get_or_create(long_url=str(payload.long_url), defaults={'expiry': payload.expiry})
            return Response({"short_code": url.short_code}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": f"{e.errors()}"}, status=status.HTTP_400_BAD_REQUEST)
