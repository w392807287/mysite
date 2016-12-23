from django.db import models
# Create your models here.


class Area(models.Model):
    name = models.CharField('名称', max_length=255, blank=True)