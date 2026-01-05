
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ai-guidance/', include('ai_guidance.urls')),
    path('api/client/', include('client.urls')),
    path('api/coach_client/', include('coach_client.urls')),
    path('api/coach_feedback/', include('coach_feedback.urls')),
    path('api/emotion-data/', include('emotion_data.urls')),
    path('api/human_coach/', include('human_coach.urls')),
    path('api/notification/', include('notification.urls')),
    path('api/', include('session_log.urls')),
    path('api/upload_resource/', include('upload_resource.urls')),
    path('api/user/', include('user.urls')),
]

