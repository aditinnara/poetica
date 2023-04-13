from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class PoemInfo(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    bio = models.CharField(max_length=200)
    profile_picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    starred = models.ManyToManyField(PoemInfo)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment_text = models.CharField(max_length=200)
    creation_time = models.DateTimeField()
    id = models.CharField(max_length=6, primary_key=True)
    poem = models.ForeignKey(PoemInfo, on_delete=models.PROTECT)
    objects = models.Manager()


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment_text = models.CharField(max_length=200)
    creation_time = models.DateTimeField()
    post = models.ForeignKey(Comment, on_delete=models.PROTECT)
    objects = models.Manager()
