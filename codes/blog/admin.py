from django.contrib import admin

from .models import Blog, Category


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    filter_horizontal = ('cates',)
    raw_id_fields = ('author',)
    search_fields = ('title', 'slug', 'text')



@admin.register(Category)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title',)