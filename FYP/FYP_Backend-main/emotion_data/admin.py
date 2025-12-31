from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import emotion_data

admin.site.register(emotion_data)
