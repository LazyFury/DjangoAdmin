from django.db import models
from django.contrib.auth.models import AbstractUser

from common.wrapped import jsonGetter

# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    @jsonGetter
    def avatar_url(self):
        return self.avatar.url if self.avatar else None