from django.urls import path
from . import views

urlpatterns = [
    path('coach-clients/', views.coachclient_list_create, name='coachclient-list'),
    path('coach-clients/<int:pk>/', views.coachclient_detail, name='coachclient-detail'),
]