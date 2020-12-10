from django.db import models


# Create your models here.
class Link(models.Model):
    """
    Класс, представляющий кастомную модель.

    link: URL-адрес
    time: Дата и время запроса адреса
    status: код ответа запроса адреса
    description: Краткое описание
    timeout: время получения ответа при запросе по адресу
    """
    link = models.URLField(unique=True, blank=False, null=False)
    time = models.DateTimeField(null=True)
    status = models.IntegerField(null=True)
    description = models.CharField(max_length=30, null=True)
    timeout = models.FloatField(null=True)

    class Meta:
        verbose_name = 'URL-Адрес'
        verbose_name_plural = 'URL-Адреса'
