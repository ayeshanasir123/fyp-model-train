from django.db import models

# Create your models here.
from django.db import models
from user.models import user

class notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Notification {self.notification_id}"
