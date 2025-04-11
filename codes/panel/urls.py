from django.urls import path, include, re_path
from . import views

app_name = 'panel'

change_info = [
    path('phone/', views.ChangePhoneUser.as_view(), name='change_phone'),
    path('email/', views.ChangeEmailUser.as_view(), name='change_email'),
    path('info/', views.ChangeBaseInfoView.as_view(), name='change_info'),
]
blog_activity = [
    path('', views.MyBlogView.as_view(), name='my_blog'),
    path('create/', views.CreateBlogView.as_view(), name='create_blog'),
    path('detail/<int:blog_id>', views.DetailBlogView.as_view(), name='detail_blog'),
    path('delete/<int:blog_id>', views.DeleteBlogView.as_view(), name='delete_blog'),
    path('update/<int:blog_id>', views.UpdateBlogView.as_view(), name='update_blog'),
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_panel'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('verify/phone/', views.VerifyPhoneView.as_view(), name='verify_phone'),
    path('change/', include(change_info)),
    path('blog/', include(blog_activity)),
]