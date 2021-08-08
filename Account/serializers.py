from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import User
from rest_framework.serializers import ValidationError
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):
    confirmpassword=serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'role', 'password','confirmpassword')
      
        extra_kwargs = {'password': {'write_only': True},'confirmpassword': {'write_only': True}}

    
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirmpassword')
        if password != confirm_password:
            raise ValidationError('Password didnt match')
        return data
    def create(self, validated_data):
        user = User.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        role=validated_data['role'],
        
        
        
        password=make_password(validated_data['password']))
        user.save()
        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password',]
