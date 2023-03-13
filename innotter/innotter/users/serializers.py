from rest_framework import serializers
from users.models import User
from django.contrib.auth import authenticate
import jwt
import datetime
from django.conf import settings

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'image']

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required")

       # Аутентификация пользователя
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if user:
            # Генерация JWT-токена
            payload = {
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
            }
            jwt_token = jwt.encode(
                payload, settings.SECRET_KEY, algorithm='HS256')
            
            data['token'] = jwt_token
            
            return data

        

class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'image', 'email', 'role', 'is_blocked' ]

class UserSerializer(serializers.ModelSerializer):
      class Meta:
        model = User
        fields = '__all__'