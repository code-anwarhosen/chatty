from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from chat.models import ChatRoom, Membership, Message
from django.contrib.auth.models import User

@login_required
def HomeView(request):
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
def UserProfileView(request, username):
    user = User.objects.filter(username=username).first()

    context = {
        'profile': user,
        'avatar': '/static/chat/icons/avatar.png'
    }
    return render(request, 'chat/pages/profile.html', context)

@login_required
def ChatRoomView(request, room_uid):
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

@login_required
def UserListView(request):
    '''
    In the home page when user click on the search bar
    this view is called by javascript fetch
    get all users list excluding current user
    return a list of all user by JsonResponse to be able to populate the search list with js
    '''
    users = User.objects.exclude(id=request.user.id).values('username')
    user_list = list()  # Convert the queryset to a list of dictionaries

    for user in users:
        user_list.append({
            'username': user['username'],
            'avatar': '/static/chat/icons/avatar.png'
        })

    return JsonResponse({'users': user_list})

@login_required
def PrivateChatRoomView(request, username):
    user_1 = request.user
    user_2 = User.objects.filter(username=username).first()
    
    # Preventing to message himself
    if user_1.username == username:
        messages.warning(request, 'You can not message yourself')
        return redirect('profile', username=user_1.username)
    
    private_room = ChatRoom.objects.filter(is_private=True, members=user_1).filter(members=user_2).first()
    if not private_room:
        private_room = ChatRoom.objects.create(is_private=True)
        private_room.members.add(user_1, user_2)
        private_room.save()
    return redirect('chatroom', room_uid=private_room.uid)