from django.contrib import admin
from .models import Image, Post, UserApp, FriendShip,Message

admin.site.register(UserApp)
admin.site.register(FriendShip)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Message)
# Register your models here.
