from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from chat.models import Profile, ChatRoom, Message
from django.contrib.auth.models import User

@login_required
def Home(request):
    user = request.user
    # alternative: rooms = ChatRoom.objects.filter(members=user)
    rooms = user.rooms.all() # works because of related_name='rooms' in ChatRoom model
    
    '''set the other_user field of private chat rooms to access the other user of the private chat room in the template'''
    for room in rooms:
        if room.is_private:
            room.second_user = room.members.exclude(id=user.id).first()
    return render(request, 'chat/pages/home.html', {'rooms': rooms})

@login_required
def UserSearchList(request):
    '''
    In the home page when user click on the search bar
    this view is called by javascript fetch
    get all users list excluding current user
    return a list of all user by JsonResponse to be able to populate the search list with js
    '''
    users = User.objects.exclude(id=request.user.id)
    user_list = list()  # Convert the queryset to a list of dictionaries

    for user in users:
        user_list.append({
            'username': user.username,
            'full_name': user.profile.full_name,
            'avatar': user.profile.avatar.url
        })
    return JsonResponse({'users': user_list})

@login_required
def InitiatePrivateChat(request, username):
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

@login_required
def ChatRoomView(request, room_uid):
    user = request.user
    chat_room = ChatRoom.objects.filter(uid=room_uid).first()

    # check if the room exists
    if not chat_room:
        messages.error(request, 'Chat Room not found. Invalid room UID.')
        return redirect('home')
    
    # check if the user is a member of the room
    if not user in chat_room.members.all():
        messages.error(request, 'You are not a member of this Chat Room.')
        return redirect('home')
    
    # alternative: room.messages.all() because of related_name='messages' in Message model
    chat_messages = Message.objects.filter(room=chat_room)
    
    chat_room.second_user = chat_room.members.exclude(id=user.id).first() if chat_room.is_private else None
    context = {
        'chat_room': chat_room,
        'chat_messages': chat_messages,
    }
    return render(request, 'chat/pages/chat_room.html', context)

@login_required
def CreateGroupChatRoom(request):
    user = request.user

    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        group_name = group_name.strip()

        if group_name:
            # check if this user already created a group by group_name
            admin_of_groups = user.admin_of_rooms.all() # return all chatroom where this user is admin
            for group in admin_of_groups:
                if group_name.lower() == group.name.lower():
                    messages.error(request, 'You already have a group by this name')
                    return redirect('home')

            # create the chat room and set admin, is_private=False mean its not a private chat between two user
            group = ChatRoom.objects.create(name=group_name, is_private=False, admin=user)
            group.members.add(user)
            group.save()

            messages.success(request, 'Group Create Successful')
            return redirect('group_profile', group_uid=group.uid)
        else:
            messages.error(request, 'Please provide a name')
    return redirect('home')

@login_required
def GroupProfile(request, group_uid):
    user = request.user
    chat_room = ChatRoom.objects.filter(uid=group_uid).first()
    
    # check if the room exists
    if not chat_room:
        messages.error(request, 'Chat Group not found. Invalid Group.')
        return redirect('home')
    
    # check if the user is a member of the room
    group_members = chat_room.members.all()
    if not user in group_members:
        messages.error(request, 'You are not a member of this Group.')
        return redirect('home')
    
    context = {
        'chat_group': chat_room,
        'chat_group_members': group_members,
    }
    return render(request, 'chat/pages/group_profile.html', context)