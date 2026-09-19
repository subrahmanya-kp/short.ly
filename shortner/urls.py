from django.urls import path
from .views import URLAdd, URLResolve

urlpatterns = [
    path('url/', URLAdd.as_view()),
    path('resolve/<str:short_code>/', URLResolve.as_view()),
]