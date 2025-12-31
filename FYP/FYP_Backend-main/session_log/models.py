
# Create your models here.
from django.db import models
from user.models import user
from client.models import client

class session_log(models.Model):
    session_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    client_id = models.ForeignKey(client, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField()

    def __str__(self):
        return f"Session {self.session_id}"
