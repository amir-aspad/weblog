from django.urls import path

from . import views

app_name = 'panel'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
]