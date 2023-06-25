from django.urls import path
from .views import *
urlpatterns = [
    path('message/<int:id>', MessageView.as_view(), name='message'),
    path('all/',MessagesView.as_view(), name='home'),
    path('send/', HandleSentMessage.as_view(), name='send'),
    path('messagesfromme', MesssagesFromUser.as_view(), name="messagesfromme"),
    path('mymessages', MessagesToUser.as_view(), name='mymessages'),
    path('view<int:id>', ReciveMessageView.as_view(), name='view'),
]