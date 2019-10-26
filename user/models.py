from django.db import models

# Create your models here.
class LoginCaptcha(models.Model):
    username = models.CharField(max_length=32)
    key = models.CharField(max_length=32)