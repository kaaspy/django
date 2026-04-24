import json
import redis.asyncio as redis
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChatRoom, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group = f"chat_{self.room_id}"

        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()

        self.redis = await redis.from_url("redis://localhost")
        await self.redis.sadd(self.room_group, self.scope.get("user").username)
        await self.channel_layer.group_send(
            self.room_group,
            {"type": "chat.users"}
        )

        messages = await self.load_history()
        for m in messages:
            await self.send(text_data=json.dumps(m))

    async def disconnect(self, code):
        self.redis = await redis.from_url("redis://localhost")
        await self.redis.srem(self.room_group, self.scope.get("user").username)
        await self.channel_layer.group_send(
            self.room_group,
            {"type": "chat.users"}
        )
        await self.redis.close()

        await self.channel_layer.group_send(
            self.room_group,
            {"type": "chat.message",
             "message": "<Left the chat>",
             "username": self.scope.get("user").username,
             "timestamp": timezone.now().strftime("%Y-%m-%d at %H:%M:%S")}
        )
        await self.channel_layer.group_discard(self.room_group, self.channel_name)

    async def receive(self, text_data = None, bytes_data = None):
        if text_data:
            data = json.loads(text_data)
            if data["type"] == "message":
                await self.save_message(data["message"])
                await self.channel_layer.group_send(
                    self.room_group,
                    {"type": "chat.message",
                     "message": data["message"],
                     "username": self.scope.get("user").username,
                     "timestamp": timezone.now().strftime("%Y-%m-%d at %H:%M:%S")}
                )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"type": "chat_message",
                                              "message": event["message"],
                                              "username": event["username"],
                                              "timestamp": event["timestamp"]}))

    async def chat_users(self, event):
        users = await self.redis.smembers(self.room_group)
        data = {"type": "userlist",
                "users": [u.decode("utf-8") for u in users]}
        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def save_message(self, content):
        chatroom = ChatRoom.objects.get(id=self.room_id)
        ChatMessage.objects.create(
            room=chatroom,
            author=self.scope.get("user"),
            content=content,
        )

    @database_sync_to_async
    def load_history(self):
        messages = ChatMessage.objects.filter(room_id=self.room_id).order_by("created")
        return [{"type": "chat_message",
                 "username": m.author.username,
                 "message": m.content,
                 "timestamp": m.created.strftime("%Y-%m-%d at %H:%M:%S")}
                for m in messages]
    
