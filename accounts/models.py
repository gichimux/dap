import imp 
from pyexpat import model
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import time
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
# from common.templatetags.common_tags import is_document_file_image


class User(AbstractUser):
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, null=True)

    def __str__(self):
        return self.username

class Profile(models.Model): 
  
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile" )
    phone_regex = RegexValidator(regex=r'^\+\d{8,15}$', message="Phone number must be entered in the format: '+254722123456'. Up to 15 digits allowed.")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(validators=[phone_regex], max_length=16, blank=True)
    avatar = models.FileField(
        max_length=1000, upload_to="profile_pics/", null=True, blank=True
    )    
    
    
    def get_fullname(self):
        if self.first_name:
            if self.last_name:
                return self.first_name + " " + self.last_name
            return self.first_name
        return self.user.username

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User) 
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()



