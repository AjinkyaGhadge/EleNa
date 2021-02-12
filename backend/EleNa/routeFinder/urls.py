from django.urls import path
from .views import find_route

urlpatterns = [
    path('', find_route)
]