from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Compaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}---{self.title}'

    class Meta:
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'


class UrlEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    email = models.EmailField()

    def __str__(self):
        return f'{self.id}---{self.url}'

    class Meta:
        verbose_name = 'UrlEmail'
        verbose_name_plural = 'UrlEmails'
