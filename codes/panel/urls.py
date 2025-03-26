from django.urls import path

from . import views

app_name = 'panel'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home_panel'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('verify/phone/', views.VerifyPhoneView.as_view(), name='verify_phone')
]