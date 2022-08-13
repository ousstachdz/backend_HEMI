from pyexpat import model
from rest_framework import serializers
from .models import FriendShip, Post, UserApp


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApp
        fields = [
            'id', 'last_login', 'username',
            'first_name', 'last_name', 'email',
            'date_joined', 'bio','profile_img','cover_img'
            ]  
        
class UserBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApp
        fields = [
            'id', 'first_name',
            'last_name', 'profile_img',
            ]  
        
        
class FriendShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendShip
        fields = '__all__'
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields = '__all__'