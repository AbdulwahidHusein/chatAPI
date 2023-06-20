from django.urls import path
from .views import *
urlpatterns = [
    path('all/',home.as_view(), name='home'),
]