from django.urls import path, re_path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.AllPostView.as_view(), name='blog_all'),
    re_path(r'^detail/(?P<slug>[\w\-\u0600-\u06FF]+)$', views.DetailBlogView.as_view(), name='detail'),
    path('comment/create/<int:blog_id>', views.CreateCommentView.as_view(), name='create_comment'),
    path('comment/reply/create/<int:blog_id>/<int:comment_id>/',
        views.CreateCommentReplyView.as_view(), name='creat_reply_comment'),
    path('/favorite/add/<int:blog_id>/', views.AddToFavoriteView.as_view() ,name='add_favorite'),
    path('/favorite/remove/<int:blog_id>/', views.RemoveToFavoriteView.as_view() ,name='remove_favorite'),
]