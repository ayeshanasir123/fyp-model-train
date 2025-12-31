from django.db import models
from human_coach.models import human_coach
from client.models import client

class coach_client(models.Model):
    coach_client_id = models.AutoField(primary_key=True)
    coach_id = models.ForeignKey(human_coach, on_delete=models.CASCADE)
    client_id = models.ForeignKey(client, on_delete=models.CASCADE)
    assigned_date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.coach_id} - {self.client_id}"

