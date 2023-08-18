from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL


class Wallet(models.Model):
    token_amount = models.IntegerField(default=30)
    owner = models.ForeignKey(
        User, related_name="owned_by", on_delete=models.CASCADE, null=True
    )  
    tips = models.ManyToManyField(
        User, blank=True, related_name="tipped_by", symmetrical=False
    )