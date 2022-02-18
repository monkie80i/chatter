from django.urls import re_path
from .consumers import NotificationConsumer
from channels.routing import ProtocolTypeRouter, URLRouter

websockets = URLRouter([
    path(
        "ws/notifications/",
        NotificationConsumer,
        name="ws_notifications",
    ),
])