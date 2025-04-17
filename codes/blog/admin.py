from django.contrib import admin
from .models import Blog, Category, Like, Follow, Comment, Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'blog')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active', 'updated')
    filter_horizontal = ('cates',)
    raw_id_fields = ('author',)
    search_fields = ('title', 'slug', 'text')
    prepopulated_fields = {'slug':('title',)}


@admin.register(Category)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_sub')
    list_filter = ('is_sub',)
    raw_id_fields = ('sub',)
    prepopulated_fields = {'slug':('title',)}


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'blog')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    raw_id_fields = ('follower', 'following')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'is_reply', 'is_active')
    raw_id_fields = ('reply', 'user', 'blog')
    search_fields = ('text',)
    list_filter = ('created', 'is_active', 'is_reply')