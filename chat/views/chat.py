import json
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import localtime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from chat.models import Profile, ChatRoom, Message, User

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
    return render(request, 'chat/pages/ChatRoom.html', context)

@login_required
def PaginatedChatMessages(request, room_uid):
    user = request.user
    chat_room = ChatRoom.objects.filter(uid=room_uid).first()

    if not chat_room:
        return JsonResponse({'success': False, 'error': "Chat room doesn't exists"})

    # Pagination parameters
    limit = int(request.GET.get('limit', 20))  # Default to 20 messages per request
    offset = int(request.GET.get('offset', 0))  # Starting point

    # Fetch messages in reverse order (latest first)
    messages = Message.objects.filter(room=chat_room).order_by('-timestamp')[offset:offset + limit]

    serialized_messages = [{
            'author': message.author.username,
            'full_name': message.author.profile.full_name,

            'avatar_url': message.author.profile.avatar.url,
            'content': message.content,
            'file_url': message.file.url if message.file else None,
            'type': message.type,
            'timestamp': localtime(message.timestamp).strftime('%d-%b %I:%M %p'), # return 20-Jan 2:40 PM
            'is_private_room': chat_room.is_private,
        } for message in messages]
    return JsonResponse({'success': True, 'messages': serialized_messages})

@login_required
def UploadChatFile(request, room_uid):
    user = request.user
    room = ChatRoom.objects.filter(uid=room_uid).first()
    
    if not room:
        return JsonResponse({'success': False, 'msg': 'Chat does not exists'})

    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            msg = Message.objects.create(room=room, author=user)
            msg.file = file
            msg.save()
            return JsonResponse({
                'success': True,
                'msgType': msg.type,
                'content': msg.file.url,
            })
    return JsonResponse({'success': False, 'msg': 'Something went wrong'})

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
    return render(request, 'chat/pages/GroupProfile.html', context)

@login_required
def UpdateGroupProfile(request, group_uid):
    group = ChatRoom.objects.filter(uid=group_uid).first()

    if not group:
        messages.error("Group doesn't exist")
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('group_name')
        avatar = request.FILES.get('group_avatar')

        if str(name).strip():
            group.name = name
        if avatar:
            group.avatar = avatar
        group.save()
        messages.success(request, "Group updated successfully!")
    return redirect('group_profile', group_uid=group_uid)

@login_required
def AddMemberSearchList(request, chatgroup_uid):
    '''
    In the Group Profile page when user click on the add member
    this view is called by javascript fetch
    get all users list excluding current user and already added member
    return a list by JsonResponse to be able to populate the add member list with js
    '''
    chat_group = ChatRoom.objects.filter(uid=chatgroup_uid).first()
    already_members = chat_group.members.all()
    
    users = User.objects.exclude(id__in=already_members)
    add_member_user_list = list()  # Convert the queryset to a list of dictionaries

    for user in users:
        add_member_user_list.append({
            'username': user.username,
            'full_name': user.profile.full_name,
            'avatar': user.profile.avatar.url
        })
    return JsonResponse({'users': add_member_user_list})

@login_required
def AddGroupMember(request):
    """Add member to a group"""
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        chatgroup_uid = data.get('chatgroup_uid')
    
        try:
            user = User.objects.get(username=username)
            chat_group = ChatRoom.objects.get(uid=chatgroup_uid)
            chat_group.members.add(user)
            chat_group.save()
            return JsonResponse({'success': True})

        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
        except ChatRoom.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Chat group not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def RemoveGroupMember(request, group_uid, username):
    group = ChatRoom.objects.filter(uid=group_uid).first()
    user = User.objects.filter(username=username).first()

    # make sure request is from group admin
    if request.user != group.admin:
        messages.info(request, "You're not a admin of this group.")
        return redirect('group_profile', group_uid=group_uid)

    # make sure doesn't remove admin himself, he can delete the group instead
    if user == group.admin:
        messages.info(request, "You can't remove the group admin.")
        return redirect('group_profile', group_uid=group_uid)
        
    if user and group:
        group.members.remove(user)
        group.save()
        messages.success(request, f'Removed {username} from this group')
    else:
        messages.error(request, 'Something went wrong!')
    return redirect('group_profile', group_uid=group_uid)

@login_required
def LeaveGroup(request, group_uid):
    user = request.user
    group = ChatRoom.objects.filter(uid=group_uid).first()
    members = group.members.all()
    
    # if admin leaving group, assain a new admin
    if user == group.admin:
        if group.member_count > 1:
            for member in members:
                if member != user:
                    group.admin = member
                    group.members.remove(user)
                    group.save()
                    messages.success(request, f"You took leave from {group.name} group")
                    return redirect('home')
        else:
            # if admin is the only user, then delete
            return redirect('delete_room', room_uid=group.uid)

    # check if requested user is in the members list or not
    elif group and user in members:
        group.members.remove(user)
        group.save()

        messages.success(request, f"You took leave from {group.name} group")
        return redirect('home')
    else:
        messages.error(request, 'Error while leaving group')
    return redirect('group_profile', group_uid=group_uid)

@login_required
def DeleteChatRoom(request, room_uid):
    user = request.user
    chat_room = ChatRoom.objects.filter(uid=room_uid).first()

    if not chat_room:
        messages.error(request, 'Chat Room does not exist')
        return redirect('home')

    # check if user is a member of the room or not
    if not user in chat_room.members.all():
        messages.info(request, "You're not a member of this group")
        return redirect('home')
    
    if chat_room.is_private:
        messages.success(request, 'private chat delete not implemented yet')
    else:
        if user == chat_room.admin:
            chat_room.delete()
            messages.success(request, 'Group delete successful')
        else:
            messages.error(request, "You can't delete this group")
    return redirect('home')