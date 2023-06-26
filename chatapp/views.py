from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message, CustomUser
from .serializers import MessageSerializer, RecievedMessageSerializer, UserCreationSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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
    permission_classes = [IsAuthenticated, IsAdminUser]

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


class UpdateMessageView(TokenObtainPairView, APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, **kwargs):
        id = self.kwargs.get('id')
        message = get_object_or_404(Message, id=id)
        if message.sender.id != request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="you cannot edit this message")
        data=request.data.copy()
        sender = request.user
        reciever_id = int(data['reciever_id'])  # Update to 'reciever_id'
        data['sender'] = sender.id
        data['reciever'] = reciever_id
        serializer = RecievedMessageSerializer(message, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data="invalid content")
    
    
class DeleteMessageView(TokenObtainPairView, APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, **kwargs):
        id = self.kwargs.get('id')
        message = get_object_or_404(Message, id=id)
        if message.reciever.id == request.user.id:
            #mark as unread if the person requesting to delete is the reciever of the message
            #I don't know why but I prefer this way
            message.recieved = False
            message.save()
            return Response(data="marked as unread")
        if message.sender.id != request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data='you can not delete this message')
        message.delete()
        return Response(status=status.HTTP_200_OK, data="message succesfully deleted")
    
class UserCreationView(APIView):
    def post(self, request):
        data = request.data.copy()
        email = data.get('email')
        try:
            if CustomUser.objects.get(email=email):
                return Response(data="the user with this email is already registered")
        except:
            serializer = UserCreationSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED, data='you have succesfully registered')
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
