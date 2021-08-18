from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer,ChangePasswordSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, logout, login


# Create your views here.
class RegisterUserAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class UserDetailedAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serialize = UserSerializer(user)
        return Response(serialize.data)


class LoginAPI(APIView):
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:

                token, created = Token.objects.get_or_create(user=user)
                # login(request,user)
                return Response({'Token key': token.key, 'Role': user.role})
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'DIC': "User does not exits or your credentials are not correct"})


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        # logout(request)
        return Response({'DIC': "User logged out"})

class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            request.user.auth_token.delete()
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)