
# Create your models here.
from django.db import models
from user.models import user
from client.models import client

class session_log(models.Model):
    session_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True)
    client_id = models.ForeignKey(client, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField(blank=True, default='')
    summary = models.TextField(null=True, blank=True)  # AI-generated conversation summary
    final_emotion = models.CharField(max_length=50, null=True, blank=True)  # Final detected emotion
    emotion_intensity = models.IntegerField(null=True, blank=True)  # Final emotion intensity

    def __str__(self):
        return f"Session {self.session_id}"
