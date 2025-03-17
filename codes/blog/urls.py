from django.urls import path, re_path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.AllPostView.as_view(), name='blog_all'),
    re_path(r'^detail/(?P<slug>[\w\-\u0600-\u06FF]+)$', views.DetailBlogView.as_view(), name='detail'),
    re_path(r'^comment/create/(?P<blog_slug>[\w\-\u0600-\u06FF]+)$',
            views.CreateCommentView.as_view(), name='create_comment'),
    re_path(
        r'^comment/reply/create/(?P<blog_slug>[\w\-\u0600-\u06FF]+)$/<int:comment_id>/',
        views.CreateCommentReplyView.as_view(), name='creat_reply_comment'),
]