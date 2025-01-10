from django.urls import path
from chat.views.auth import UserLoginView, UserLogoutView, UserRegisterView
from chat.views.chat import HomeView, UserProfileView, UserListView, ChatRoomView, PrivateChatRoomView

urlpatterns = [
    path('auth/login/', UserLoginView, name='login'),
    path('auth/register/', UserRegisterView, name='register'),
    path('auth/logout/', UserLogoutView, name='logout'),

    path('', HomeView, name='home'),
    path('room/<str:room_uid>/', ChatRoomView, name='chatroom'),
    path('user-list/', UserListView, name='user_list'),
    path('profile/<str:username>/', UserProfileView, name='profile'),
    path('private-chat/<str:username>/', PrivateChatRoomView, name='private_room'),
]
