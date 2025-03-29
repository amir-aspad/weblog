from django.urls import path,include
from . import views

app_name = 'panel'

change_info = [
    path('phone/', views.ChangePhoneUser.as_view(), name='change_phone'),
    path('email/', views.ChangeEmailUser.as_view(), name='change_email'),
    path('info/', views.ChangeBaseInfoView.as_view(), name='change_info'),
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_panel'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('verify/phone/', views.VerifyPhoneView.as_view(), name='verify_phone'),
    path('change/', include(change_info))
]