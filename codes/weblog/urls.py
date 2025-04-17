from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', include('panel.urls', namespace='panel')),
    path('', include('blog.urls', namespace='blog')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.LANGUAGE_CODE == 'fa':
    admin.site.site_header = 'مدیریت پروژه'
    admin.site.site_title = 'پنل مدیریت'
    admin.site.index_title = 'به پنل مدیریت خوش آمدید'