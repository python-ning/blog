# coding:utf-8

from django.conf.urls import include, url
from django.contrib import admin
from blog.upload import upload_image
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r"^uploads/(?P<path>.*)$",\
        "django.views.static.serve",\
        {"document_root": settings.MEDIA_ROOT,}),
    # 配置上传路径
    url(r'^admin/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
    url(r'^', include('blog.urls')),
]
