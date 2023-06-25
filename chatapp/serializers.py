from rest_framework import serializers
from rest_framework.fields import EmailField, CharField, FileField, ImageField
from .models import Message
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    name = CharField(source='first_name',required=True)
    email= EmailField(required=True)
    class Meta:
        model = CustomUser
        exclude = ['password',]
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