from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user_info', views.user_info, name='user_info'),
    path('register/', views.register, name='register'),
    path('change_passage/', views.change_password, name='change_password'),
    path('change_email/', views.change_email, name='change_email'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    path('forget_password/', views.forget_password, name='forget_password')
]