from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    bio = models.CharField(max_length=200)
    profile_picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    starred = models.JSONField(default=list)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment_text = models.CharField(max_length=200)
    creation_time = models.DateTimeField()
    poem_id = models.IntegerField(blank=True, null=True)


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    reply_text = models.CharField(max_length=200)
    creation_time = models.DateTimeField()
    comment = models.ForeignKey(Comment, on_delete=models.PROTECT)
