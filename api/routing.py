from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<username>\w+)/$', consumers.ChatConsumer.as_asgi())
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/notification/$', consumers.NotificationConsumer.as_asgi()),
    # re_path(r'ws/notification/(?P<id>\w+)/$', consumers.NotificationConsumer.as_asgi()),
]
