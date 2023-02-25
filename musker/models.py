from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

TOOL_CHOICES = (
    ("PYTHON", "Python"),
    ("CSHARP", "C#"),
    ("C", "C"),
    ("CPP", "C++"),
    ("JS", "JavaScript"),
    ("PHP", "PHP"),
    ("SWIFT", "Swift"),
    ("JAVA", "Java"),
    ("GO", "Go"),
    ("RUBY", "Ruby"),
    ("HTML", "HTML"),
    ("CSS", "CSS"),
    ("KOTLIN", "Kotlin"),
    ("SCALA", "Scala"),
    ("RUST", "Rust"),
    ("PERL", "Perl"),
    ("MATHLAB", "Mathlab"),
    ("TYPESCRIPT", "TypeScript"),
    ("R", "R"),
    

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
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.TextField(blank=False, max_length=1000)
    description = models.TextField(blank=False, max_length=9999999999999999999)
    tool = models.CharField(
        max_length = 20,
        choices = TOOL_CHOICES,
        default = None
        )
    max_capacity = models.IntegerField(blank=False, default=1)
    current_capacity = models.IntegerField(blank=False, default=0)
    isFull = models.BooleanField(blank=False, default=False)
    if(current_capacity == max_capacity):
        isFull = True
    join = models.ManyToManyField(User, related_name="joined_by", symmetrical=False, blank=True)
    
    def __str__(self):
        return self.title     
    
