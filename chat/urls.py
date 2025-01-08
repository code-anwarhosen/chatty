from django.urls import path
from chat.views.auth import user_login, user_logout, user_register
from chat.views.chat import home, chat_room

urlpatterns = [
    path('', home, name='home'),
    path('auth/login/', user_login, name='login'),
    path('auth/logout/', user_logout, name='logout'),
    path('auth/register/', user_register, name='register'),

    path('room/<str:room_uid>/', chat_room, name='chatroom'),
]
