import jwt
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Отключение middleware в случае логина в админ-панель
        current_url = request.path
        if 'admin/' in current_url:
            return self.get_response(request)
        
        # Получение JWT-токена из заголовка Authorization или куки
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if not jwt_token:
            jwt_token = request.COOKIES.get('jwt_token')
        if not jwt_token:
            request.user = AnonymousUser()
            return self.get_response(request)
        jwt_token = jwt_token.replace(settings.JWT_AUTH_HEADER_PREFIX + ' ', '')

        # Декодирование JWT-токена
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError:
            request.user = AnonymousUser()
            return self.get_response(request)

        # Проверка времени жизни токена
        if 'exp' in payload and datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
            request.user = AnonymousUser()
            return self.get_response(request)

        # Поиск пользователя по ID, указанному в токене
        User = get_user_model()
        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            request.user = AnonymousUser()
            return self.get_response(request)

        # Аутентификация пользователя
        request.user = user
        return self.get_response(request)

