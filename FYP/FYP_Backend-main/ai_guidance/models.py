from django.db import models

class ai_guidance(models.Model):
    guidance_id = models.AutoField(primary_key=True)
    
    # Check if you have these two lines:
    client_id = models.ForeignKey('client.client', on_delete=models.CASCADE, null=True)
    session_id = models.ForeignKey('session_log.session_log', on_delete=models.CASCADE, null=True)
    
    emotion_id = models.ForeignKey('emotion_data.emotion_data', on_delete=models.CASCADE)
    suggestion = models.TextField()
    effectiveness = models.IntegerField(default=0)
    user_message = models.TextField(null=True, blank=True)
    ai_response = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Guidance {self.guidance_id}"