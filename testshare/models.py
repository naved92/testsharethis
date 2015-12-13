from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserProfile(models.Model):
    """Model referring to user profile,based on the top of django User model
    about_me->about me text about the user
    picture->profile picture of the user
    last_location->last location of the user

    """
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    pw=models.CharField(max_length=10, blank=True)
    about_me = models.CharField(blank=True, max_length=300)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    last_location = models.CharField(blank=True, max_length=300)
    verification_status_choices = (
        ('a', 'active'),
        ('d', 'deactive'),
        ('o', 'other'),
        ('p', 'pending'),
        ('s', 'suspended')
    )
    verification_status = models.CharField(blank=False, max_length=2, choices=verification_status_choices, default='p')
    verification_code = models.CharField(blank=False, max_length=128, default='123456')

    def __unicode__(self):
        return self.user.username


class Location(models.Model):
    """
    Model referring to the different locations of the users.
    """
    location_name = models.CharField(blank=True, max_length=300)
    location_lat = models.FloatField(blank=True, null=True)
    location_long = models.FloatField(blank=True, null=True)


#class Log(models.Model):
#    logger = models.ForeignKey(UserProfile)
#    logtext = models.CharField(blank=True, max_length=50)
#    timestamp = models.DateTimeField(blank=True)



class Post(models.Model):
    """
    Model referring to the user posts.
    """
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
    """
    Model referring to the blocks
    """
    blocker = models.ForeignKey(UserProfile, related_name='user_who_blocked')
    blocked = models.ForeignKey(UserProfile, related_name='user_who_got_blocked')
    block_time = models.DateTimeField(blank=True)


class Profileposts:
    """
    A helper class for rendering profile posts
    """
    def __init__(self):
        self.post_info = Post()
        self.alignment=""