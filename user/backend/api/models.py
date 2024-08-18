from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.email} - Token: {self.token}"