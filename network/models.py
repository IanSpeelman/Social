from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=9999)
    timestamp = models.DateTimeField(default=timezone.now())

class Follow(models.Model):
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")