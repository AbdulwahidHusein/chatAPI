from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message
from .serializers import MessageSerializer
# Create your views here.

class home(APIView):
    serialiser_class = MessageSerializer
    messages = Message.objects.all()
    serialized = MessageSerializer(messages, many=True)
    def get(self, request):
        message = Message.objects.all()[0]
        serialized = MessageSerializer(message).data
        return Response(serialized)
