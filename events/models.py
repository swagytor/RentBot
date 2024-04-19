from django.db import models


# Create your models here.
class Event(models.Model):
    start_date = models.DateTimeField(verbose_name="Начало")
    end_date = models.DateTimeField(verbose_name="Конец")
    court = models.ForeignKey('courts.Court', on_delete=models.CASCADE, verbose_name="Корт")
    player = models.ForeignKey('players.Player', on_delete=models.CASCADE, verbose_name="Игрок")

    def __str__(self):
        return f"{self.player} {self.start_date}"

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
