from django.db import models


# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    rank = models.CharField(max_length=4, verbose_name="NTRP-рейтинг", blank=True, null=True)
    tg_id = models.CharField(max_length=100, verbose_name="ID в Telegram")
    tg_username = models.CharField(max_length=100, verbose_name="Ник в Telegram", blank=True, null=True)
    is_premium = models.BooleanField(verbose_name="Премиум", default=False)
    is_notify_about_games = models.BooleanField(verbose_name="Уведомлять о играх", default=False)
    is_notify_about_changes = models.BooleanField(verbose_name="Уведомлять о изменениях", default=False)

    def __str__(self):
        return self.name
