from django.urls import path
from chat.views.auth import UserLogin, UserLogout, UserRegister, UserProfile, EditUserProfile, UpdateUserProfile
from chat.views.chat import Home, UserSearchList, InitiatePrivateChat, ChatRoomView

urlpatterns = [
    path('auth/login/', UserLogin, name='login'),
    path('auth/register/', UserRegister, name='register'),
    path('auth/logout/', UserLogout, name='logout'),
    path('auth/user/profile/<str:username>/', UserProfile, name='profile'),
    path('auth/user/edit-profile/', EditUserProfile, name='edit_profile'),
    path('auth/user/update-profile/', UpdateUserProfile, name='update_profile'),

    path('', Home, name='home'),
    path('user-list/', UserSearchList, name='user_list'),
    path('private-chat/<str:username>/', InitiatePrivateChat, name='private_room'),
    path('room/<str:room_uid>/', ChatRoomView, name='chatroom'),
]
