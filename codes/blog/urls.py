from django.urls import path, re_path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.AllPostView.as_view(), name='blog_all'),
    re_path(r'^detail/(?P<slug>[\w\-\u0600-\u06FF]+)$', views.DetailBlogView.as_view(), name='detail'),
]