from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message, CustomUser
from .serializers import MessageSerializer, RecievedMessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404


def authenticate_user(email, password):
    try:
        user= CustomUser.objects.get(email=email, password=password)
        if user:
            return user
        else:
            raise AuthenticationFailed("invalid credentiallls")
    except:
        raise AuthenticationFailed("invalid credentials2")
    

class MessageView( TokenObtainPairView,APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        id = self.kwargs.get('id')
        message = Message.objects.filter(id=id)
        serialized_data = MessageSerializer(message, many=True).data
        return Response(serialized_data)


class MessagesView(TokenObtainPairView, APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.all()
        serialized_data = MessageSerializer(messages, many=True).data
        return Response(serialized_data)


class HandleSentMessage(TokenObtainPairView, APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        sender = request.user
        reciever_id = int(data['reciever_id'])  # Update to 'reciever_id'
        reciever = CustomUser.objects.get
        data['sender'] = sender.id
        data['reciever'] = reciever_id
        reciever = get_object_or_404(CustomUser, id=reciever_id)
        serialized_data = RecievedMessageSerializer(data=data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(status=status.HTTP_202_ACCEPTED,data=f"message succesfully sent to {reciever.first_name}!")
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
                   
class MesssagesFromUser(TokenObtainPairView, APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        messages = Message.objects.filter(sender=user)
        serialized_data = MessageSerializer(messages, many=True).data
        return Response(serialized_data)

class MessagesToUser(TokenObtainPairView, APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        messages = Message.objects.filter(reciever=user)
        serialized_data = MessageSerializer(messages, many=True).data
        return Response(serialized_data)
    
class ReciveMessageView(TokenObtainPairView, APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, **kwargs):
        id = self.kwargs.get('id')
        message = get_object_or_404(Message, id=id)
        if message.reciever == request.user:
            message.recieved = True
            message.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_304_NOT_MODIFIED)