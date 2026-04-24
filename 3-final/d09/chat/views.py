import json
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, ChatMessage

class ChatRoomListView(ListView):
    model = ChatRoom
    template_name = "chatroom_list.html"
    context_object_name = "chatrooms"

@login_required(login_url="/account")
def chatroom(request, pk):
    ctx = {}
    ctx.update(chatroom=get_object_or_404(ChatRoom, id=pk))

    return render(request, "room.html", ctx)
