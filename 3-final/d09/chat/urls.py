from django.urls import path
from . import views

urlpatterns = [
    path("chatrooms", views.ChatRoomListView.as_view(), name="chatrooms"),
    path("room/<int:pk>", views.chatroom, name="chatroom"),
]    
