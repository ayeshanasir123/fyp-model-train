
from django.db import models

class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

