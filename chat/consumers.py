import json 

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncConsumer

class ChatConsumer(AsyncConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] #get the argument room_name 

        