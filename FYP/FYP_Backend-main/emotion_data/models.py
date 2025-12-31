from django.db import models

# DO NOT import serializers here!
# DO NOT import views here!

class emotion_data(models.Model):
    emotion_id = models.AutoField(primary_key=True)
    # Use string references for foreign keys to prevent circular loops
    client_id = models.ForeignKey('client.client', on_delete=models.CASCADE)
    session_id = models.ForeignKey('session_log.session_log', on_delete=models.CASCADE)
    emotion = models.CharField(max_length=50)
    intensity = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emotion} - {self.intensity}%"