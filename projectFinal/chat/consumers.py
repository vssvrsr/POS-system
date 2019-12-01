import datetime
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings

from .models import Message
from appFinal.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['shop_id']

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        now_time = datetime.datetime.now().strftime(settings.DATETIME_FORMAT)

        if not message:
            return

        Message.objects.create(
            user=User.objects.get(user_id=text_data_json['user_id']), message=message, group_name=self.room_group_name)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'now_time': now_time
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        now_time = event['now_time']
        user_id = event['user_id']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'now_time': now_time,
        }))
