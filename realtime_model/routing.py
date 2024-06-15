from django.urls import path

from realtime_model import consumers

ws_urlpatterns = [
    path("ws/ml_model/", consumers.Consumer.as_asgi())
]