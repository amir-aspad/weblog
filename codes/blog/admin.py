from django.contrib import admin

from .models import Blog, Category, Like


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
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