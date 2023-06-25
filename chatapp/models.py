from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    second_name = models.CharField(max_length=50, null=True, blank=True)
    age  = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='files/images/profile_pictures')
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recieved = models.BooleanField(default=False)
    sent_date = models.DateTimeField(auto_now_add=True)
    recieved_date = models.DateTimeField(default=None, null=True, blank=True)
    file = models.FileField(upload_to='files', null=True , blank=True)
    image = models.ImageField(upload_to='files/images/message_pictures', null=True, blank=True)
    text = models.TextField()
    
    def __str__(self):
        return self.sender.email + ' to '+ self.reciever.email
        
    