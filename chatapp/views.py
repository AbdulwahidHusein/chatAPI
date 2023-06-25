from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message, CustomUser
from .serializers import MessageSerializer, LoginSerializer, CustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


def authenticate_user(email, password):
    try:
        user= CustomUser.objects.get(email=email, password=password)
        if user:
            return user
        else:
            raise AuthenticationFailed("invalid credentiallls")
    except:
        raise AuthenticationFailed("invalid credentials2")
    
class MessageView(TokenObtainPairView, APIView):
    authentication_classes = [TokenObtainPairView]
    permission_classes = [IsAuthenticated]
    def get(self, request, **kwargs):
        id = self.kwargs.get(id)
        message  = Message.objects.filter(id=id)
        serialized_data = MessageSerializer(message).data
        return Response(serialized_data)


class MessagesView(TokenObtainPairView, APIView):
    authentication_classes = [TokenObtainPairView]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        messages = Message.objects.filter()
        serialized_data = MessageSerializer(messages, many=True).data
        return Response(serialized_data)

class HandleSentMessage(TokenObtainPairView, APIView):
    authentication_classes = [TokenObtainPairView]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.POST
        serialized_data = MessageSerializer(data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(status.HTTP_202_ACCEPTED)
        else:
            return Response(status.HTTP_406_NOT_ACCEPTABLE)
        
class MesssagesFromUser(TokenObtainPairView, APIView):
    authentication_classes = [TokenObtainPairView]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        messages = Message.objects.filter(sender=user)
        serialized_data = MessageSerializer(messages, many=True)
        return Response(serialized_data)

class MessagesToUser(TokenObtainPairView, APIView):
    authentication_classes = [TokenObtainPairView]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        messages = Message.objects.filter(reciever=user)
        serialized_data = MessageSerializer(messages, many=True)
        return Response(serialized_data)

class LoginView(APIView):
     def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('second_name')

            # Perform authentication and generate token
            # Example code using Django's built-in authentication
            user = authenticate_user(email, password)
            if user is not None:
                refresh = RefreshToken.for_user(user)

                response = Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                    })
                response.set_cookie('jwt', refresh.access_token, httponly=True)
                response.data = {
                    'user': CustomUserSerializer(user).data
                                }
                return response
            else:
                return Response({'error': 'Invalid credentials3'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LogoutView(APIView):
    def get(self, request):
        # Delete the token associated with the user
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
class GetMessage(APIView):
    authentication_classes = []
    
        