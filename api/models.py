from django.db import models
from django.contrib.auth.models import AbstractUser

class UserApp(AbstractUser):
    bio = models.TextField(default='hello world')
    profile_img = models.ImageField(upload_to='./static/profile',null=True, blank=True)
    cover_img = models.ImageField(upload_to='./static/cover',null=True, blank=True)


class FriendShip(models.Model):
    sender = models.ForeignKey(UserApp, on_delete=models.CASCADE,related_name='+')
    reciever = models.ForeignKey(UserApp, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return (self.sender.username+" and "+self.reciever.username)

class Post(models.Model):
    owner = models.ForeignKey(UserApp, on_delete=models.CASCADE, related_name='owner')
    content = models.TextField(blank=True)
    timestamp = models.DateField(auto_now_add=True)
    public = models.BooleanField(default=False)
    only_friends = models.BooleanField(default=True)
    private = models.BooleanField(default=False)
    has_image = models.BooleanField(default=False)
    has_multi_images = models.BooleanField(default=False)

    def __str__(self):
        return self.content
    

class Image(models.Model):
    
    is_profile = models.BooleanField(default=False)
    is_cover = models.BooleanField(default=True)
    is_post = models.BooleanField(default=False)
    owner = models.ForeignKey(UserApp, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True, blank=True)
    cover_img = models.ImageField(upload_to='./static/images',null=True, blank=True)

    def __str__(self) -> str:
        return self.owner.username
    
    
class Message(models.Model):
    sender = models.ForeignKey(UserApp, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(UserApp, on_delete=models.CASCADE, related_name='reciever')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self) -> str:
        return self.content
    
