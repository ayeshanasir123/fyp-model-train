from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.sessionlog_list_create, name='session-list'),
    path('sessions/<int:pk>/', views.sessionlog_detail, name='session-detail'),
]