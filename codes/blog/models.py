from django.conf import settings
from django.db import models

from .managers import PostManager

class BaseModle(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Category(BaseModle):
    sub = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_category',
        blank=True, null=True
    )
    is_sub = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Blog(BaseModle):
    baner = models.ImageField(upload_to='blog')
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    cates = models.ManyToManyField(Category, related_name='blogs')
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    objects = models.Manager()
    config = PostManager
    

    class Meta:
        ordering = ('-updated', '-created',)
        verbose_name = 'بلاگ'
        verbose_name_plural = 'بلاگ ها'

