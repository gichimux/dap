from django.db import models
from django.utils import timezone

from django.conf import settings
User = settings.AUTH_USER_MODEL
from posts.models import Post

class Alert(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_alerts')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_alerts')
    ALERT_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('reply', 'Reply'),
    )
    alert_type = models.CharField(max_length=10, choices=ALERT_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)  # If the alert is related to a post
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} {self.alert_type}d your post'

    class Meta:
        ordering = ['-timestamp']