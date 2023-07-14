import json 

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message
from django.utils.timesince import timesince
from .templates.app.components.template_tags import initials

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
    
    async def receive(self, text_data):
        # Receive message from WebSocket (front end)
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        name = text_data_json['name']
        agent = text_data_json.get('agent', '')
    
        
        print('Receive:', type)

        if type == 'message':
            new_message = await self.create_message(name, message, agent)

            # Send message to group / room
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'chat_message',
                    'message': message,
                    'name': name,
                    'agent': agent,
                    'initials': initials(name),
                    'created_at': timesince(new_message.created_at),
                }
            )
        elif type == 'update':
            print('is update')
            # Send update to the room
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'writing_active',
                    'message': message,
                    'name': name,
                    'agent': agent,
                    'initials': initials(name),
                }
            )

    @sync_to_async
    def get_room(self):
        self.room = Room.objects.get(uuid = self.room_name)

    @sync_to_async
    def create_message(self, sent_by, message):
        message = Message.objects.create(body = message, sent_by=sent_by)
    

    