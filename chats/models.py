from django.db import models
from accounts.models import Profile
from django.utils import timezone
import math

# Create your models here.


class ThreadFeed(models.Model):
    pass

class Thread(models.Model):
    
    thread_by = models.ForeignKey(
        Profile, related_name="thread_by", on_delete=models.CASCADE, null=True
    ) 
    headline = models.CharField(max_length=20)
    story = models.CharField(max_length=500)
    
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
        return self.product_name


class ThreadLike(models.Model):
    thread = models.ForeignKey(
        Thread, related_name="thread_likes", on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        Profile, related_name="profile_thread_likes", on_delete=models.CASCADE, null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)


class ThreadComment(models.Model):
    comment_by = models.ForeignKey(
        Profile, related_name="commented_by", on_delete=models.CASCADE, null=True
    )
    related_post = models.ForeignKey(
        Thread, related_name="thread_comment", on_delete=models.CASCADE
    )
    comment_image = models.ImageField(upload_to='images/')

    comment = models.CharField(max_length=300)

class ThreadReply(models.Model):
    reply_by = models.ForeignKey(
        Profile, related_name="replied_by", on_delete=models.CASCADE, null=True
    )
    related_comment = models.ForeignKey(
        Comment, related_name="thread_comment_reply", on_delete=models.CASCADE
    )
    reply_image = models.ImageField(upload_to='images/')

    comment = models.CharField(max_length=300)


class ReThread(models.Model):
    rethread_by = models.ForeignKey(
        Profile, related_name="profile_rethread", on_delete=models.CASCADE, null=True
    )
    original_thread = models.ForeignKey(
        Thread, related_name="original_thread", on_delete=models.CASCADE, null=True
    )

class ThreadImage(models.Model):
    img_name = models.CharField(max_length=255, null=True)
    thread = models.ForeignKey(
        Thread, related_name="for_thread", on_delete=models.CASCADE
        )
    image = models.ImageField(upload_to='images/')
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.img_name