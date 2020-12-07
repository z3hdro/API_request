from django.db import models

# Create your models here.
class Link(models.Model):
    link = models.URLField(unique=True, blank=False, null=False)
    time = models.DateTimeField(null=True)
    status = models.IntegerField(null=True)
    ip = models.CharField(unique=True, max_length=20, null=True)
    timeout = models.TimeField(null=True)
