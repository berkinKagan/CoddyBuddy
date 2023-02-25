from django.contrib import admin
from django.contrib.auth.models import Group,User
from .models import Profile, Post

# Register your models here.
admin.site.unregister(Group)
admin.site.register(Post)

class ProfileInline(admin.StackedInline):
    model = Profile
    
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username","email","password"]
    inlines = [ProfileInline]
    

admin.site.unregister(User)
admin.site.register(User, UserAdmin)    