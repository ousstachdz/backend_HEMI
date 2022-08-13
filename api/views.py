from re import U
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import FriendShip, Post, UserApp
from .serializers import FriendShipSerializer, PostSerializer, UserBasicInfoSerializer, UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def test(request):
     print(request.user)
     return Response( data='good', status= status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
     user = UserApp.objects.get(id=request.user.id)
     serializer = UserSerializer(user) 
     return Response( data=serializer.data, status= status.HTTP_200_OK)
     
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friend_list(request):
     friend_ships_list =( 
               FriendShip.objects.all().filter(sender=request.user.id) |
               FriendShip.objects.all().filter(reciever=request.user.id)
          )
     friend_list = []
     for friend_ship in friend_ships_list :
          if friend_ship.sender.id == request.user.id:
               print('true')
               friend_list.append(friend_ship.reciever)
          else:
               print('false')
               friend_list.append(friend_ship.sender)
     serializer = UserBasicInfoSerializer(friend_list, many=True)
     return Response( data=serializer.data, status= status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post(request):
     posts = Post.objects.filter(owner=request.user.id)
     serializer = PostSerializer(posts, many=True)
     return Response(data=serializer.data,status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_id(request,pk):
     try:
          user = UserApp.objects.get(id=pk)
          if user :
               serializer = UserSerializer(user)
               data=serializer.data 
     except:
          data = {'response':'out of range'}
     return Response( data=data, status= status.HTTP_200_OK)