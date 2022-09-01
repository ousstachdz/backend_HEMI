from asyncio.windows_events import NULL
from copyreg import constructor
import math
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination 
from rest_framework_simplejwt.tokens import RefreshToken

from .models import  Conversation, FriendShip, Message, Post, UserApp
from .serializers import ( 
               ConversationSerializer, MessageSerializer, PostSerializer, UserBasicInfoSerializer, 
               UserCreatSerializer, UserSerializer
                    )


@api_view(['POST'])
def signup_step_one(request):
     print(request.data)
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

# get the user for the profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
     user = UserApp.objects.get(id=request.user.id)
     serializer = UserSerializer(user) 
     return Response( data=serializer.data, status= status.HTTP_200_OK)

# todo set the user login online
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_online(request):
     return Response(data={'name':'oussama'}, status=status.HTTP_200_OK)

# get the list of friends 
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

# get the publication of user 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post(request, pk):
     posts = Post.objects.filter(owner=pk)
     if post :
          if str(request.user.id) == pk:
               serializer = PostSerializer(posts, many=True)
               return Response(data=serializer.data,status=status.HTTP_200_OK)
          
          friend_ship = FriendShip.objects.get_for(user_=pk,user__=request.user.id)

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

# get the publication for the home 
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
     sender =  request.user.id
     reciever = pk
     conversation = Conversation.objects.get_for(user_=reciever, user__=sender)
     if (len(conversation)<=0):
          reciever_ = UserApp.objects.get(id=reciever)
          sender_ = UserApp.objects.get(id=sender)
          conversation =[]
          conversation.append(Conversation.objects.create(owner=sender_, reciever= reciever_ ))     

          conversation[0].save()
          
     serializer = ConversationSerializer(conversation[0], )

     conversation_id= { 'conversation_id' : serializer.data['id']}
     context = {
          **conversation_id,
          'sender_id' : sender,
          
     }
     return Response(data=context , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, pk):
     messages = Message.objects.get_for(user_=request.user.id,user__=pk)
     serializer = MessageSerializer(messages, many=True)
     return Response(data=serializer.data , status=status.HTTP_200_OK)


@api_view(['post'])
@permission_classes([IsAuthenticated])
def complet_setup_first_step(request):
     user = UserApp.objects.get(id=request.user.id)
     if(request.data['birthdate']):
          user.birthdate= request.data['birthdate']
     user.address= request.data['address']
     user.complete_setup += 33
     user.save()
     return Response(data={},status=status.HTTP_200_OK)

     
@api_view(['post'])
@permission_classes([IsAuthenticated])
def complet_setup(request):
     user = UserApp.objects.get(id=request.user.id)
     # print(request.data)
     # print(request.files)
     user.bio= request.data['bio']
     user.profile_img= base64_file(request.data['profile_img'],'profile')
     user.cover_img = base64_file(request.data['cover_img'],'cover')
     user.complete_setup += 34
     user.save()
     return Response(data={},status=status.HTTP_200_OK)

import base64
from django.core.files.base import ContentFile


def base64_file(data, name=None):
    _format, _img_str = data.split(';base64,')
    _name, ext = _format.split('/')
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))