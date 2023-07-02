import json 

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] #get the argument room_name 
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        await self.get_room()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        return await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    

    @sync_to_async
    def get_room(self):
        self.room = Room.objects.get(uuid = self.room_name)

    @sync_to_async
    def create_message(self, sent_by, message):
        message = Message.objects.create(body = message, sent_by=sent_by)
    

    