from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE,  blank=True, null = True , related_name="posted_by")
    post = models.CharField(max_length=140)
    timestamp =  models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField( User,  blank=True, related_name="totallikes")
  
    def __str__(self):
        return f"{self.id} by {self.user}"

class Profile(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE,  blank=True, null = True , related_name="user_profile")
    follower = models.ManyToManyField( User,  blank=True, related_name="user_followers")
    following = models.ManyToManyField( User,  blank=True, related_name="user_following")
    
    def __str__(self):
        return f"{self.user} is following {self.following}"