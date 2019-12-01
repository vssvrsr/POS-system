# chat/urls.py
from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    # 各店聊天室
    path('', views.room, name='room'),

    # 測試websocket
    #path('', views.index, name='index'),
    #path('<str:room_name>/', views.room, name='room'),

    # 在線人員列表
    #path('chat/', views.chat, name='chat'),

]
