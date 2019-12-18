from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:shop_id>/', consumers.ChatConsumer),
]
