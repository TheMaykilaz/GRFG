from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import JSONField

class CryptoToken(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=20, unique=True)  # Додано unique=True
    price = models.DecimalField(max_digits=20, decimal_places=2)
    percent_1h = models.FloatField()
    percent_24h = models.FloatField()
    percent_7d = models.FloatField()
    market_cap = models.DecimalField(max_digits=25, decimal_places=2)
    volume_24h = models.DecimalField(max_digits=25, decimal_places=2)
    sparkline_7d = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name} ({self.symbol})"
    
    class Meta:
        ordering = ['-market_cap'] 


class CryptoArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)


class ForumTopic(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name='topics')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comments.count()

class ForumComment(models.Model):
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, default=1, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    vote_count = models.IntegerField(default=0)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.email} on {self.topic.title}"

class ForumCommentVote(models.Model):
    comment = models.ForeignKey(ForumComment, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()

    class Meta:
        unique_together = ('comment', 'user')  