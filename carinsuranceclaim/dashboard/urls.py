from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("<str:claim_no>",views.details,name="details")
]
