from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import User
from rest_framework.serializers import ValidationError
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'role','image', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create(
        username = validated_data['username'],
        role = validated_data['role'],
        image = validated_data['image'],
        password = make_password(validated_data['password']))
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

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
