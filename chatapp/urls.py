from django.urls import path
from .views import *
urlpatterns = [
    path('message/<int:id>', MessageView.as_view(), name='message'),
    path('all/',MessagesView.as_view(), name='home'),
    path('send', HandleSentMessage, name='send'),
]