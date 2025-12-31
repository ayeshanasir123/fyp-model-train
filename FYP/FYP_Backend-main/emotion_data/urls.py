from django.urls import path
from . import views

urlpatterns = [
    path('', views.emotion_list_create, name='emotion-list-create'),
]