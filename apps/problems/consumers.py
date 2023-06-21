import json

from channels.generic.websocket import AsyncWebsocketConsumer


class AttemptConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = "attempt"

    async def connect(self):
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    # Receive message from room group
    async def attempt_message(self, event):
        print(event)
        # Send message to attempts WebSocket
        await self.send(text_data=json.dumps(event))


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group
        room_group_name = self.scope["url_route"]["kwargs"]["user_id"]
        await self.channel_layer.group_add(str(room_group_name), self.channel_name)
        await self.accept()

    # Receive message from room group
    async def user_submission_info(self, event):
        print("user_message")
        # Send message to attempts WebSocket
        print(event)

        await self.send(text_data=json.dumps(event))
