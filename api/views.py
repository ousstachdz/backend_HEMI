import math
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination 
from rest_framework_simplejwt.tokens import RefreshToken

from .models import  FriendShip, Message, Post, UserApp
from .serializers import ( 
               MessageSerializer, PostSerializer, UserBasicInfoSerializer, 
               UserCreatSerializer, UserSerializer
                    )
from api import serializers


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
     user = UserApp.objects.get(id=request.user.id)
     serializer = UserSerializer(user) 
     return Response( data=serializer.data, status= status.HTTP_200_OK)
     
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friend_list(request, pk):
     friend_ships_list =( 
               FriendShip.objects.all().filter(sender=pk) |
               FriendShip.objects.all().filter(reciever=pk)
          )
     friend_list = []
     for friend_ship in friend_ships_list :
          if str(friend_ship.sender.id) == pk:
               friend_list.append(friend_ship.reciever)
          else:
               friend_list.append(friend_ship.sender)
     serializer = UserBasicInfoSerializer(friend_list, many=True)
     return Response( data=serializer.data, status= status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post(request, pk):
     posts = Post.objects.filter(owner=pk)
     if post :
          if str(request.user.id) == pk:
               serializer = PostSerializer(posts, many=True)
               return Response(data=serializer.data,status=status.HTTP_200_OK)
          
          friend_ship = (
               (FriendShip.objects.all().filter(sender=pk)
               &FriendShip.objects.all().filter(reciever=request.user.id))|
               (FriendShip.objects.all().filter(reciever=pk)
               &FriendShip.objects.all().filter(sender=request.user.id))
               )
          
          if (friend_ship):
               posts = (posts.filter(only_friends=True)|posts.filter(public=True))
          
          serializer = PostSerializer(posts, many=True)
          return Response(data=serializer.data,status=status.HTTP_200_OK)
     return Response(data={},status=status.HTTP_200_OK)

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_post(request):
     serializer = PostSerializer(data=request.data)
     if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_post(request):
     PAGE_SIZE = 10
     paginator= PageNumberPagination()
     paginator.page_size = PAGE_SIZE
     post_list = Post.objects.all().order_by('timestamp')
     num_pages = (math.floor(post_list.count()/PAGE_SIZE))+1
     num_this_pages = int(request.GET.get('page'))
     if num_this_pages<=num_pages:
          post_list = paginator.paginate_queryset(post_list, request)
          serializer = PostSerializer(post_list, many=True)
          return Response(data={'num_this_pages':num_this_pages,'num_pages':num_pages, 'post_list':serializer.data}, status=status.HTTP_200_OK)
     return Response(data={'message':'out of range'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation(request,pk):
     print(pk)
     print(request.user.id)
     message = (
          (Message.objects.all().filter(sender=pk)& Message.objects.all().filter(reciever=request.user.id))|
          (Message.objects.all().filter(sender=request.user.id)& Message.objects.all().filter(reciever=pk))
          )
     
     if (len(message)>0):
          serializer = MessageSerializer(message,many=True)
          return Response(data=serializer.data , status=status.HTTP_200_OK)
     return Response( status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def signup_step_one(request):
     password = request.data['password']
     confirm_password = request.data['confirm_password']
     if password == confirm_password:
          serializer = UserCreatSerializer(data=request.data)
          if serializer.is_valid():
               user = serializer.save()
               refresh = RefreshToken.for_user(user)
               data= {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
               return Response(data=data , status= status.HTTP_200_OK)
     return Response( data=serializer.errors, status= status.HTTP_400_BAD_REQUEST)