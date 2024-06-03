from django.db import models

from common.models import Model

# Create your models here.
class Dict(Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    group = models.ForeignKey('DictGroup', on_delete=models.CASCADE, related_name='dicts')

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'Dictionary'
        verbose_name_plural = 'Dictionaries'

class DictGroup(Model):
    name = models.CharField(max_length=255, unique=True)
    key = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def dicts(self):
        return self.dicts.all()

    class Meta:
        verbose_name = 'Dictionary Group'
        verbose_name_plural = 'Dictionary Groups'