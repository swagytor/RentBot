from django.db import models


# Create your models here.
class Court(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    address = models.CharField(max_length=256, verbose_name="Адрес", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Корт"
        verbose_name_plural = "Корты"
