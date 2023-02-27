import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms

TOOL_CHOICES = (
    ("Python"),
    ("C#"),
    ("C"),
    ("C++"),
    ("JavaScript"),
    ("PHP"),
    ("Swift"),
    ("Java"),
    ("Go"),
    ("Ruby"),
    ("HTML"),
    ("CSS"),
    ("Kotlin"),
    ("Scala"),
    ("Rust"),
    ("Perl"),
    ("Mathlab"),
    ("TypeScript"),
    ("R"),
    

)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'profile_images', default = 'default-profile-image-png-1-Transparent-Images.png')
    bio = models.TextField(default="You add your biography", blank=True, max_length=9999999999999999999999999)
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False,
                                     blank=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender = User)
def create_profile(sender, instance, created,**kwargs):
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
        
class Post(models.Model):
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    title = models.TextField(blank=False, max_length=1000)
    description = models.TextField(blank=False, max_length=9999999999999999999)
    tool = models.CharField(max_length=10, default=None)
    max_capacity = models.IntegerField(blank=False, default=1)
    current_capacity = models.IntegerField(blank=False, default=1)
    capacityRatio = models.FloatField(blank = False,default=0)
    
    isFull = models.BooleanField(blank=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    if(current_capacity == max_capacity):
        isFull = True
    join = models.ManyToManyField(User, related_name="joined_by", symmetrical=False, blank=True)
    
    def __str__(self):
        return self.title
    
    def __init__(self,*args,**kwargs):
        super(Post, self).__init__(*args, **kwargs)
        if self.max_capacity is not None:
            self.capacityRatio = (self.current_capacity/self.max_capacity)*100
    
