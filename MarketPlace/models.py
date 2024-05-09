from datetime import timezone, datetime
from django.contrib.auth.models import User
from django.db import models

class cliente (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self
class loja (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
         return self