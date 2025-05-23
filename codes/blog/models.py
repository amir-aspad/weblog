from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse
from django.db import models

# thir party importing
from django_ckeditor_5.fields import CKEditor5Field

from .managers import ActiveManager, FristCommentManager

class BaseModle(models.Model):
    title = models.CharField(_("عنوان"), max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True)

    def __str__(self):
        return self.title[:30]


    class Meta:
        abstract = True


class Category(BaseModle):
    sub = models.ForeignKey(
        'self', verbose_name=_('زیر مجموعه دسته بندی'),  on_delete=models.CASCADE,
        related_name='sub_category', blank=True, null=True
    )
    is_sub = models.BooleanField(_('وضعیت زیر مجموعه بودن'), default=False)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Blog(BaseModle):
    baner = models.ImageField(_('بنر'), upload_to='blog')
    text = CKEditor5Field(_('متن'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('نویسنده'),  on_delete=models.CASCADE, related_name='blogs'
    )
    cates = models.ManyToManyField(Category, verbose_name=_("دسته بندی"), related_name='blogs')
    is_active = models.BooleanField(_('وضعیت انتشار'), default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ'))
    
    objects = models.Manager()
    config = ActiveManager()

    def can_add_to_favorite(self, request):
        '''check user can add to favorite or no'''
        if not request.user.is_authenticated:
            return True
        return not self.favorites.filter(blog=self, user=request.user).exists()

    def can_like(self, request):
        '''check user can like blog or no'''
        if not request.user.is_authenticated:
            return True
        return not self.blog_like.filter(user=request.user).exists()
    
    def like_count(self):
        '''count all like for especial blog'''
        return self.blog_like.count()
    
    def comments_count(self):
        '''count all comments for especial blog'''
        return self.comments.filter(is_active=True).count()

    def related_blog(self):
        '''find related blog. just look at categories'''
        return Blog.config.filter(cates__in=self.cates.all()).exclude(id=self.id).distinct()[:5]
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug':self.slug})
    
    def get_panel_detail_blog_url(self):
        return reverse('panel:detail_blog', kwargs={'blog_id':self.id})


    class Meta:
        ordering = ('-is_active', '-updated')
        verbose_name = 'بلاگ'
        verbose_name_plural = 'بلاگ ها'

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('کاربر'),  on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name=_('بلاگ'), related_name='blog_like')

    def __str__(self):
        return f'user {self.user} like blog {self.blog}'
    

    class Meta:
        verbose_name = 'لایک'
        verbose_name_plural = 'لایک ها'


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('دنبال کننده'),
        on_delete=models.CASCADE, related_name='followers'
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('دنبال شونده'),
        on_delete=models.CASCADE, related_name='followings'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ'))
    
    def __str__(self):
        return f'user {self.follower.phone} follow {self.following.phone}'


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('کاربر'), on_delete=models.CASCADE, related_name='comments'
    )
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, verbose_name=_('بلاگ'), related_name='comments'
    )
    reply = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name=_('در پاسخ به'),
        related_name='rcomments',  blank=True, null=True
    )
    is_reply = models.BooleanField(_('وضعیت پاسخ'), default=False)
    text = CKEditor5Field(_('متن کامنت'), max_length=250, config_name='simple')
    is_active = models.BooleanField(_('وضعیت انتشار'), default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ'))

    objects = models.Manager()
    config = FristCommentManager()

    def __str__(self):
        return self.text[:30]
    

    def reply_comments(self):
        return self.rcomments.filter(is_active=True)


    class Meta:
        ordering = ('-created',)
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f'{self.user} - {self.blog}'
    

    class Meta:
        verbose_name = 'علاقه مندی'
        verbose_name_plural = 'علاقه مندی ها'