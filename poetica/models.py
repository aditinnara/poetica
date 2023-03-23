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
