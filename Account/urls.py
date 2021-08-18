from django.urls import path
from .views import RegisterUserAPI,UserDetailedAPI,LoginAPI,LogoutAPI,ChangePasswordView
from rest_framework.authtoken.views import obtain_auth_token

app_name='Account'
urlpatterns = [
    
    path('register/',RegisterUserAPI.as_view(),name='register'),
    path('login/',LoginAPI.as_view(),name='login'),
    path('logout/',LogoutAPI.as_view(),name='logout'),
    path('api/users/profile/',UserDetailedAPI.as_view(),name='userdetail'),
    path('api/changepassword/', ChangePasswordView.as_view(), name='change-password'),
    
    
]
