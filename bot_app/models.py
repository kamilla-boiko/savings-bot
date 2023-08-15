from django.db import models


class TelegramUser(models.Model):
    user_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    username = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}"


class Saving(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}: {self.amount} ({self.user.username})"
