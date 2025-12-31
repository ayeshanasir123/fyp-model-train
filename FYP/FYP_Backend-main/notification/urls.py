from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.notification_list_create, name='notification-list'),
    path('notifications/<int:pk>/', views.notification_detail, name='notification-detail'),
]