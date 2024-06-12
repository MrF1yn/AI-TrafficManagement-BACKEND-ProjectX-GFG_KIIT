from django.urls import path

from realtime_model import consumers

ws_urlpatterns = [
    path("ws/test/", consumers.Consumer.as_asgi())
]