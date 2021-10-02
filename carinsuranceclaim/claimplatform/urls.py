from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
    path("user1/",views.index,name="index"),
    path("user2/",views.user,name="user"),
    path("post_create/",views.post_create,name='post_create'),
    path("table/",views.table,name="table")
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)