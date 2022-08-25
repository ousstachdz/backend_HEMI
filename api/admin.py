from django.contrib import admin
from .models import Conversation, Image, Post, UserApp, FriendShip,Message

admin.site.register(UserApp)
admin.site.register(FriendShip)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Message)
admin.site.register(Conversation)
# Register your models here.
