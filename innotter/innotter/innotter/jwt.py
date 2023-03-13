import jwt
from datetime import datetime, timedelta
from django.conf import settings
from users.models import User

def encode_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')

def decode_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])
        return user
    except (jwt.DecodeError, User.DoesNotExist):
        return None