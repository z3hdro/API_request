from django.db import models


# Create your models here.
class Link(models.Model):
    link = models.URLField(unique=True, blank=False, null=False)
    time = models.DateTimeField(null=True)
    status = models.IntegerField(null=True)
    description = models.CharField(max_length=30, null=True)
    timeout = models.TimeField(null=True)

    class Meta:
        verbose_name = 'URL-Адрес'
        verbose_name_plural = 'URL-Адреса'
