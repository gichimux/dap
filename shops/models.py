from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.core.validators import RegexValidator

class Size(models.TextChoices):
     S = 'S', 'S'
     M = 'M', 'M'
     L = 'L', 'L'
     XL = 'XL', 'XL'
     XXL = 'XXL', 'XXL'

# Model for Merchandise
class Merch(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    color = models.CharField(max_length=50)
    size = models.CharField(
        max_length=50,
        choices=Size.choices,
        default=Size.M
    )  
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

# Model for Merchandise Images
class MerchImage(models.Model):
    merch = models.ForeignKey(Merch, related_name='merch_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='merch_images/')

    def __str__(self):
        return f"Image for {self.merch.name}"