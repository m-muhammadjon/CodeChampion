from django.urls import path

from apps.problems import consumers

websocket_urlpatterns = [
    path("ws/attempt-socket", consumers.AttemptConsumer.as_asgi()),
    path("ws/user-socket/<int:user_id>", consumers.UserConsumer.as_asgi()),
]