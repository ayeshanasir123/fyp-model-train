from django.urls import path
from . import views
from . import dataset_export

urlpatterns = [
    # Removing 'ai-guidance/' from here because it's already in the main urls.py
    path('', views.aiguidance_list_create, name='ai-guidance-list'),
    path('<int:pk>/', views.aiguidance_detail, name='ai-guidance-detail'),
    
    # Dataset export endpoints for training
    path('dataset/export/', dataset_export.export_for_training, name='dataset-export'),
    path('dataset/stats/', dataset_export.dataset_stats, name='dataset-stats'),
]