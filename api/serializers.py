from rest_framework import serializers

from .models import FriendShip, Message, Post, UserApp



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
    # owner = serializers.PrimaryKeyRelatedField(queryset = UserApp.objects.all())
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


class MessageSerializer(serializers.ModelSerializer):
    sender = UserBasicInfoSerializer()
    reciever = UserBasicInfoSerializer()

    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        
        sender_data = validated_data.pop('sender')
        reciever_data = validated_data.pop('reciever')
        reciever = UserApp.objects.get(id = reciever_data)
        sender = UserApp.objects.get(id = sender_data)
        
        message = Message.objects.create(**validated_data)
        message.sender = sender
        message.reciever = reciever
        
        return message