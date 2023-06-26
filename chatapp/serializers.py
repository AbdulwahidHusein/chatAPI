from rest_framework import serializers
from rest_framework.fields import EmailField, CharField, FileField, ImageField, IntegerField
from .models import Message
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    first_name = CharField(required=True)
    #email= EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'second_name', 'age', 'country', 'profile_picture'
        ]
class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer()
    reciever = CustomUserSerializer()
    file = serializers.FileField()
    class Meta:
        model = Message
        fields = '__all__'
        
class RecievedMessageSerializer(serializers.ModelSerializer):
    image = ImageField(required=False)
    file = FileField(required=False)
    text = CharField( required=True)
    class Meta:
        model = Message
        fields = [
            'text', 'image', 'file', 'sender', 'reciever'
            
        ]

class UserCreationSerializer(serializers.ModelSerializer):
    email = EmailField(required=True)
    password = CharField(required=True)
    first_name = CharField(required=True)
    second_name = CharField(required=False)
    age = IntegerField(required=False)
    country = CharField(required=False)
    profile_picture = FileField(required=False)
    class Meta:
        model = CustomUser
        fields = [
            'email','password', 'first_name', 'second_name', 'age', 'country', 'profile_picture'
        ]