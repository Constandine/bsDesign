from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    msg = models.CharField(max_length=200)
    fr = models.CharField(max_length=30)
    to = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    href = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    img = models.CharField(max_length=200)

class Userprofile(models.Model):
    face = models.CharField(max_length=30)
    user = models.OneToOneField(User)
    likes = models.ManyToManyField(Like)
