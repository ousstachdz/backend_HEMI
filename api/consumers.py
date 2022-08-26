import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from api.serializers import MessageSerializer, UserBasicInfoSerializer
from api.models import Conversation, Message, UserApp


class ChatConsumer(AsyncWebsocketConsumer):
    
    def connect(self):
        return super().connect()
    
    async def disconnect(self, code):
        print('disconnect')
        return super().disconnect(code)
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        id =text_data_json['conversation_id']
        
        chat_room = f'conversation__{id}'
        self.chat_room =chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        
        message = await self.save_message(text_data_json)
        
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type':'send_message',
                'message':message
            }
        
        )
        
    async def send_message(self,event):
        await self.send(json.dumps({
                    "event": event
                })
        )

    @database_sync_to_async
    def save_message(self,text_data_json):

        print(text_data_json)
        conversation =Conversation.objects.get(id=text_data_json['conversation_id'])
        sender = UserApp.objects.get(id=text_data_json['sender_id'])
        message = Message.objects.create(conversation=conversation,content= text_data_json['message'],sender=sender)
        sender_serializer = UserBasicInfoSerializer(sender)
        message_serializer = MessageSerializer(message)
        json_message=  json.dumps({'message':message_serializer.data,'sender':sender_serializer.data})
        # json_message=  {'message':message_serializer.data,'sender':sender_serializer.data}
        return json_message
        