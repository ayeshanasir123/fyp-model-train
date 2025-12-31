

from django.db import models
from user.models import user

class human_coach(models.Model):
    coach_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

