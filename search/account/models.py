from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    search = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.search}'

    class Meta:
        verbose_name = 'Поиск'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=512)
    ide = models.CharField(max_length=512)
    url = models.CharField(max_length=512)
    duration = models.CharField(max_length=32)
    thumbnail = models.CharField(max_length=512)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Корзина'


class VideoInfo(models.Model):
    search = models.ForeignKey(Video, on_delete=models.CASCADE)
    title = models.CharField(max_length=512)
    ide = models.CharField(max_length=512)
    url = models.CharField(max_length=512)
    duration = models.CharField(max_length=32)
    thumbnail = models.CharField(max_length=512)









