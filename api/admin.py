from django.contrib import admin
from .models import Image, Post, UserApp, FriendShip

admin.site.register(UserApp)
admin.site.register(FriendShip)
admin.site.register(Post)
admin.site.register(Image)
# Register your models here.
