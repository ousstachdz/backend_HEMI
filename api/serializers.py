from email import message
from rest_framework import serializers

from .models import Conversation, FriendShip, Message, Post, UserApp



class UserCreatSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    class Meta:
        model=UserApp
        fields = '__all__'
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.pop('username')
        user = UserApp.objects.create_user(
            username=username,
            password=password,
            **validated_data
        )

        return user


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
    owner = UserBasicInfoSerializer()
    
    class Meta:
        model= Post
        fields = '__all__'
    
    def create(self, validated_data):
        owner_data = validated_data.pop('owner')
        owner = UserApp.objects.get(id = owner_data)
        post = Post.objects.create(**validated_data)
        post.owner = owner
        return post


class ConversationSerializer(serializers.ModelSerializer):
    owner = UserBasicInfoSerializer()
    reciever = UserBasicInfoSerializer()

    class Meta:
        model = Conversation
        fields = '__all__'

    def create(self, validated_data):
        owner_data = validated_data.pop('owner')
        reciever_data = validated_data.pop('reciever')
        owner = UserApp.objects.get(id = owner_data)
        reciever = UserApp.objects.get(id = reciever_data)
        conversation = Conversation.objects.create(**validated_data)
        conversation.reciever = reciever
        conversation.owner = owner
        return conversation

    
class MessageSerializer(serializers.ModelSerializer):
    conversation = ConversationSerializer()
    sender = UserBasicInfoSerializer()

    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        sender_data = validated_data.pop('sender')
        sender = UserApp.objects.get(id = sender_data)
        message = Message.objects.get(**validated_data)
        message.sender = sender
        return message