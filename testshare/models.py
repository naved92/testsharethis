from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    pw = models.CharField(blank=True, max_length=10);
    # The additional attributes we wish to include.
    about_me = models.CharField(blank=True, max_length=300)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    last_location = models.CharField(blank=True, max_length=300)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class Location(models.Model):
    location_name = models.CharField(blank=True, max_length=300)
    location_lat = models.FloatField(blank=True, null=True)
    location_long = models.FloatField(blank=True, null=True)


class Log(models.Model):
    logger = models.ForeignKey(UserProfile)
    logtext = models.CharField(blank=True, max_length=50)
    timestamp = models.DateTimeField(blank=True)



class Post(models.Model):
    post_maker = models.ForeignKey(UserProfile)
    post_text = models.CharField(blank=True, max_length=300)
    post_photo = models.ImageField(upload_to='post_images/', blank=True)
    post_location = models.ForeignKey(Location, blank=True, null=True)
    post_time = models.DateTimeField(blank=True, null=True)
    post_sharedfrom = models.ForeignKey('self', blank=True, null=True)
    post_sharecount = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-post_time']



class Block(models.Model):
    blocker = models.ForeignKey(UserProfile, related_name='user_who_blocked')
    blocked = models.ForeignKey(UserProfile, related_name='user_who_got_blocked')
    block_time = models.DateTimeField(blank=True)


class Profileposts:
    def __init__(self):
        self.post_info = Post()
        self.alignment=""