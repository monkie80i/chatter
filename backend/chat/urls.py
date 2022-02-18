from django.urls import path
from . import views

# Urls here

urlpatterns = [
    path('',views.index, name='index'),
]