from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    name = models.CharField(
        max_length=64,
        null=False,
        unique=True,
    )
    description = models.CharField(
        max_length=256,
    )

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    author = models.ForeignKey(
        User,
        db_column="user",
        on_delete=models.CASCADE,
        null=False,
        related_name="users",
    )
    room = models.ForeignKey(
        ChatRoom,
        db_column="room",
        on_delete=models.CASCADE,
        null=False,
        related_name="messages",
    )
    created = models.DateTimeField(
        null=False,
        auto_now_add=True,
    )
    content = models.TextField(
    )

    def __str__(self):
        return self.content
