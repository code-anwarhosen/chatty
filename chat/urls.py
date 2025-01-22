from django.urls import path
from chat.views.auth import (
    UserLogin, UserLogout, UserRegister, UserProfile, 
    EditUserProfile, UpdateUserProfile, ChangeUserPassword
)
from chat.views.chat import (
    Home, UserSearchList, InitiatePrivateChat, ChatRoomView, PaginatedChatMessages,
    UploadChatFile, CreateGroupChatRoom, GroupProfile, UpdateGroupProfile, AddGroupMember,
    AddMemberSearchList, RemoveGroupMember, LeaveGroup, DeleteChatRoom,
)

urlpatterns = [
    path('auth/login/', UserLogin, name='login'),
    path('auth/register/', UserRegister, name='register'),
    path('auth/logout/', UserLogout, name='logout'),
    path('auth/user/profile/<str:username>/', UserProfile, name='profile'),
    path('auth/user/edit-profile/', EditUserProfile, name='edit_profile'),
    path('auth/user/update-profile/', UpdateUserProfile, name='update_profile'),
    path('auth/user/change-password/', ChangeUserPassword, name='change_password'),

    path('', Home, name='home'),
    path('user-list/', UserSearchList), # js fetch call from home page search modal
    path('private-chat/<str:username>/', InitiatePrivateChat, name='private_room'),
    path('room/<str:room_uid>/', ChatRoomView, name='chatroom'),
    path('chat/<str:room_uid>/messages/', PaginatedChatMessages, name='get_chat_messages'),
    path('chat/send-file/<str:room_uid>/', UploadChatFile),

    path('user/group/create/', CreateGroupChatRoom, name='create_group'),
    path('user/group/details/<str:group_uid>/', GroupProfile, name='group_profile'),
    path('user/group/update/<str:group_uid>/', UpdateGroupProfile, name='update_group'),
    path('group/add-member-user-list/<str:chatgroup_uid>/', AddMemberSearchList), # js fetch call to list user to add member
    path('user/group/add-member/', AddGroupMember), # js fetch call from group page modal
    path('user/group/remove-member/<str:group_uid>/<str:username>/', RemoveGroupMember, name='remove_member'),
    path('user/group/leave-group/<str:group_uid>/', LeaveGroup, name='leave_group'),
    path('user/group/delete-room/<str:room_uid>/', DeleteChatRoom, name='delete_room'),
]
