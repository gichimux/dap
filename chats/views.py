from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from posts.models import *
from .models import *
# Create your views here.


@login_required
def chat_list(request):
    chats = Room.objects.all()
    context ={
        'chats': chats,
   }    
    return render(request, "chats/chatlist.html", context)


@login_required
def chat_room(request, room_name ):
    room, created = Room.objects.get_or_create(name=room_name)
    messages = Message.objects.filter(room=room)[0:25]

    context ={
        'room': room,
        'messages': messages,

   }    
    return render(request, "chats/room.html", context)

