from django.db import models
from accounts.models import Profile
from django.utils import timezone
import math
# from forums.models import Forum
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.

class Condition(models.TextChoices):
        NEW = 'New', "NEW"
        WELL_USED = 'Well used', "WELL_USED"
        USED = 'Used', "USED"
        SCRAP = 'Scrap', "SCRAP"
        
class HashTag(models.Model):
    name = models.URLField(max_length=100)

   
class Post(models.Model):
    post_image = models.ImageField(upload_to='images/', null=True, blank=True,)
    posted_by = models.ForeignKey(
        User, related_name="posted_by", on_delete=models.CASCADE, null=True
    )     
    hashtag = models.ManyToManyField(
        HashTag, blank=True, related_name="hash_tag"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts", symmetrical=False)
    dislikes = models.ManyToManyField(User, blank=True, related_name="disliked_posts", symmetrical=False)
    comment_count = models.IntegerField(default=0)
    
    headline = models.CharField(max_length=100, blank=True)
    
    body = models.TextField() 


    def upvote(self, user):
        self.likes.add(user)
        self.dislikes.remove(user)
        self.save()

    def downvote(self, user):
        self.likes.remove(user)
        self.dislikes.add(user)
        self.save()

    @property
    def vote_count(self):
        likes = self.likes.count()
        dislikes = self.dislikes.count()
        votes = likes - dislikes
        return votes
    
    
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
                return str(seconds) +  "s"
            
            else:
                return str(seconds) + " s"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + "m"
            
            else:
                return str(minutes) + "m"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + "h"

            else:
                return str(hours) + "h"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + "d"

            else:
                return str(days) + "d"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + "mo"

            else:
                return str(months) + "mo"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + "yr"

            else:
                return str(years) + "yrs"



    class Meta:
        ordering = ["timestamp"]

    def __int__(self):
        return self.id



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
    parent_post = models.ForeignKey(
        Post, related_name="parent_post", on_delete=models.CASCADE
    )

    body = models.CharField(max_length=500)
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
                return str(seconds) +  "s"
            
            else:
                return str(seconds) + " s"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + "m"
            
            else:
                return str(minutes) + "m"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + "h"

            else:
                return str(hours) + "h"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + "d"

            else:
                return str(days) + "d"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + "mo"

            else:
                return str(months) + "mo"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + "yr"

            else:
                return str(years) + "yrs"

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return self.related_post

class Reply(models.Model):
    reply_by = models.ForeignKey(
        User, related_name="reply_by", on_delete=models.CASCADE, null=True
    )
    related_comment = models.ForeignKey(
        Comment, related_name="post_comment_reply", on_delete=models.CASCADE
    )

    body = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.timestamp

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "s"
            
            else:
                return str(seconds) + " s"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + "m"
            
            else:
                return str(minutes) + "m"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + "h"

            else:
                return str(hours) + "h"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + "d"

            else:
                return str(days) + "d"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + "mo"

            else:
                return str(months) + "mo"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + "yr"

            else:
                return str(years) + "yrs"

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return self.related_comment

class RePost(models.Model):
    reposted_by = models.ForeignKey(
        User, related_name="profile_repost", on_delete=models.CASCADE, null=True
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
                return str(seconds) +  "s"
            
            else:
                return str(seconds) + " s"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + "m"
            
            else:
                return str(minutes) + "m"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + "h"

            else:
                return str(hours) + "h"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + "d"

            else:
                return str(days) + "d"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + "mo"

            else:
                return str(months) + "mo"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + "yr"

            else:
                return str(years) + "yrs"
            
    def __str__(self):
        return self.original_post

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user