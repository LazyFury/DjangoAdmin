import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from common.wrapped import jsonGetter

# Create your models here.
class Model(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser,Model):
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
    
    def get_all_permissions(self):
        groups = self.groups.all()
        group_permissions = [permission for group in groups for permission in group.permissions.all()]
        user_permissions = self.user_permissions.all()
        permission = set()
        for p in group_permissions+list(user_permissions):
            permission.add(p)
        return permission
    

class UserToken(Model):
    pass