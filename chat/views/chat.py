from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from chat.models import ChatRoom, Membership, Message

@login_required
def home(request):
    user = request.user
    rooms = ChatRoom.objects.filter(members=user) # alternative: rooms = user.rooms.all() because of related_name='rooms' in ChatRoom model
    
    '''
    set the other_user field of private chat rooms to access the other user of the private chat room in the template
    '''
    for room in rooms:
        if room.is_private:
            room.other_user = room.members.exclude(id=user.id).first()
    
    return render(request, 'chat/pages/home.html', {'rooms': rooms})

@login_required
def chat_room(request, room_uid):
    user = request.user
    room = ChatRoom.objects.filter(uid=room_uid).first()

    # check if the room exists
    if not room:
        messages.error(request, 'Room not found. Invalid room UID.')
        return redirect('home')
    
    # check if the user is a member of the room
    if not user in room.members.all():
        messages.error(request, 'You are not a member of this room.')
        return redirect('home')
    
    chat_messages = Message.objects.filter(room=room) # alternative: room.messages.all() because of related_name='messages' in Message model
    context = {
        'chat_room': room,
        'chat_messages': chat_messages,
        'is_private': room.is_private,
        'other_user': room.members.exclude(id=user.id).first() if room.is_private else None,
    }
    return render(request, 'chat/pages/chat_room.html', context)