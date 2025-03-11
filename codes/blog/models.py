from django.conf import settings
from django.db import models

from .managers import PostManager

class BaseModle(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Category(BaseModle):
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Blog(BaseModle):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    cates = models.ManyToManyField(Category, related_name='blogs')
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    baner = models.ImageField(upload_to='blog')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    objects = models.Manager()
    config = PostManager
    

    class Meta:
        ordering = ('-updated', '-created')
        verbose_name = 'بلاگ'
        verbose_name_plural = 'بلاگ ها'

