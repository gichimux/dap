from django.db import models
from accounts.models import Profile
from django.utils import timezone
import math

from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.

class Condition(models.TextChoices):
        NEW = 'New', "NEW"
        WELL_USED = 'Well used', "WELL_USED"
        USED = 'Used', "USED"
        SCRAP = 'Scrap', "SCRAP"
        
class Pick_Up(models.TextChoices):
        MEETUP = 'Meetup', "MEETUP"
        ON_PREMISE = 'On Premise', "ON_PREMISE"

class Post_Type(models.TextChoices):
        SELL = 'Sell', "SELL"
        SWAP = 'Swap', "SWAP"

class Payment_Method(models.TextChoices):
        MPESA = 'Mpesa ', "MPESA"
        CASH = 'Cash', "CASH"        

 

class Feed(models.Model):
    pass

class Post(models.Model):

    posted_by = models.ForeignKey(
        User, related_name="posted_by", on_delete=models.CASCADE, null=True
    )     
    post_location = models.CharField(max_length=100, default="Mombasa")

    
    timestamp = models.DateTimeField(auto_now_add=True)
    product_condition = models.CharField(max_length=50,
        choices=Condition.choices,
        default=Condition.NEW
        )
    post_type = models.CharField(max_length=50,
        choices=Post_Type.choices,
        default=Post_Type.SELL
        )
    about = models.CharField(max_length=100)
    sale_price = models.IntegerField(default=0)
    gold_price = models.IntegerField(default=0)

    product_pick_up = models.CharField(max_length=50,
        choices=Pick_Up.choices,
        default=Pick_Up.MEETUP
        )
    payment_method = models.CharField(max_length=50,
        choices=Payment_Method.choices,
        default=Payment_Method.MPESA
        )
    likes = models.ManyToManyField(
        User, blank=True, related_name="liked_by", symmetrical=False
    )

    @property
    def total_likes(self):
        return self.likes.count()
    
    # @property
    def poster_full(self):
        le_profile = Profile.objects.get(user=self.posted_by)
        name = le_profile.name
        return name
     
    def poster_bio(self):
        le_profile = Profile.objects.get(user=self.posted_by)
        bio = le_profile.bio
        return bio

    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.timestamp

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"



    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return self.post_location

   
class Like(models.Model):
    post = models.ForeignKey(
        Post, related_name="post_likes", on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        User, related_name="profile_likes", on_delete=models.CASCADE, null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post
    
class Comment(models.Model):
    comment_by = models.ForeignKey(
        User, related_name="comment_by", on_delete=models.CASCADE, null=True
    )
    related_post = models.ForeignKey(
        Post, related_name="post_comment", on_delete=models.CASCADE
    )

    comment = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    def poster_full(self):
        related = self.related_post.posted_by
        le_profile = Profile.objects.get(user=related)
        name = le_profile.name
        return name
     
    def poster_bio(self):
        le_profile = Profile.objects.get(user=self.posted_by)
        bio = le_profile.bio
        return bio

    def related_poster(self):
        related = self.related_post.posted_by
        le_profile = Profile.objects.get(user=related)
        return le_profile
    
    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.timestamp

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return self.related_post

class Reply(models.Model):
    reply_by = models.ForeignKey(
        Profile, related_name="reply_by", on_delete=models.CASCADE, null=True
    )
    related_comment = models.ForeignKey(
        Comment, related_name="post_comment_reply", on_delete=models.CASCADE
    )

    comment = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.timestamp

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return self.related_comment

class RePost(models.Model):
    reposted_by = models.ForeignKey(
        Profile, related_name="profile_repost", on_delete=models.CASCADE, null=True
    )
    original_post = models.ForeignKey(
        Post, related_name="original_post", on_delete=models.CASCADE, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.timestamp

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"
    def __str__(self):
        return self.original_post
    
class PostImage(models.Model):
    img_name = models.CharField(max_length=255, null=True)
    post = models.ForeignKey(
        Post, related_name="for_product", on_delete=models.CASCADE
        )
    image = models.ImageField(upload_to='images/')
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.img_name

