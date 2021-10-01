from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("post_create/",views.post_create,name='post_create'),
    path("table/",views.table,name="table")
    
]
