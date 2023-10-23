from django.urls import path
from .views import *
urlpatterns = [
    path('', Menu.as_view())
]