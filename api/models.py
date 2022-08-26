from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser

class UserApp(AbstractUser):
    bio = models.TextField(default='hello world')
    profile_img = models.ImageField(upload_to='./static/profile',null=True, blank=True)
    cover_img = models.ImageField(upload_to='./static/cover',null=True, blank=True)


class FriendShipManager(models.Manager):
    
    def get_for(self, user_,user__):
        friend_ship = (
            Q(Q(sender=user_)&Q(reciever=user__))|
            Q(Q(reciever=user_)&Q(sender=user__))
            )
        return super().get_queryset().filter(friend_ship)
    
    
class FriendShip(models.Model):
    sender = models.ForeignKey(UserApp, on_delete=models.CASCADE,related_name='+')
    reciever = models.ForeignKey(UserApp, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)
    objects = FriendShipManager()
    
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
    owner = models.ForeignKey(UserApp, on_delete=models.CASCADE, related_name='+')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True, blank=True)
    cover_img = models.ImageField(upload_to='./static/images',null=True, blank=True)

    def __str__(self) -> str:
        return self.owner.username
    
    
class ConversationManager(models.Manager):
    
    def get_for(self, user_,user__):
        friend_ship = (
            Q(Q(reciever=user_)&Q(owner=user__))|
            Q(Q(owner=user_)&Q(reciever=user__))
            )
        return super().get_queryset().filter(friend_ship) 


class Conversation(models.Model):
    owner = models.ForeignKey(UserApp, on_delete=models.CASCADE, )
    reciever = models.ForeignKey(UserApp, on_delete=models.CASCADE, related_name='reciever')
    objects= ConversationManager()
    
    
class MessageManager(models.Manager):
    
    def get_for(self, user_,user__):
        friend_ship = (
            Q(Q(conversation__reciever=user_)&Q(conversation__owner=user__))|
            Q(Q(conversation__owner=user_)&Q(conversation__reciever=user__))
            )
        return super().get_queryset().filter(friend_ship) 
    
    
class Message(models.Model):
    sender = models.ForeignKey(UserApp, on_delete=models.CASCADE, related_name='sender')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='+')
    objects = MessageManager()
    
    def __str__(self) -> str:
        return self.content
    
