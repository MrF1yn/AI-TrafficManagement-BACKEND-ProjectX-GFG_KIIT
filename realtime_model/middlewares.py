
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken, TokenError

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class WebSocketJWTAuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        authorization_token = None

        # Iterate through headers to find 'authorization' key
        for key, value in scope["headers"]:
            if key == b'authorization':
                authorization_token = value.decode('utf-8').split(' ')[1]  # Extract token part after 'Bearer '
                break

        token = authorization_token

        try:
            access_token = AccessToken(token)
            scope["user"] = await get_user(access_token["user_id"])
            return await self.app(scope, receive, send)
        except TokenError:
            scope["user"] = AnonymousUser()

        return None

