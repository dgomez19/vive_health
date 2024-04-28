from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginUserGetJWT.as_view(), name='security-login-api'),
    path('users/<uuid:uuid>/login/', views.LoginUserAPIView.as_view(), name='security-users-login-api'),

    path('users/', views.UserListCreateAPIView.as_view(), name='security-users-api'),
    path('users/<uuid:uuid>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='security-users-api'),
    path('users/roles/', views.RolesUserListAPIView.as_view(), name='security-users-roles-api'),
    path('users/generate-password/<uuid:uuid>/', views.UserGeneratePasswordAPIView.as_view(),
         name='security-users-generate-password'),
    path('profile/', views.ProfileView.as_view(), name='security-profile'),
    path('users/forgot-password/', views.UserForgotPasswordAPIView.as_view(), name='security-users-forgot-password')
]
