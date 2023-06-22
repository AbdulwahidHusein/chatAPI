from django.urls import path
from .views import *
urlpatterns = [
    path('all/',MessagesView.as_view(), name='home'),
]