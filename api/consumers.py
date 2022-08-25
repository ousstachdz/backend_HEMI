import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from api.serializers import MessageSerializer

from api.models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    
    def connect(self):
        return super().connect()
    
    async def disconnect(self, code):
        print('disconnect')
        return super().disconnect(code)
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = await self.send_message(text_data_json)
        print(message)
        await self.send(json.dumps({'data':'message'}))
        

    @database_sync_to_async
    def send_message(self,text_data_json):

        print(text_data_json['conversation_id'])
        conversation =Conversation.objects.get(id=text_data_json['conversation_id'])
        
        message = Message.objects.create(conversation=conversation,content= text_data_json['message'])

        return message
        