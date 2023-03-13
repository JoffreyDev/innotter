import datetime
from django.conf import settings
from django.http import JsonResponse

import jwt
from users.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from rest_framework.decorators import action
from django.contrib.auth import authenticate


class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], serializer_class=UserRegisterSerializer)
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                User.objects.create_user(username=serializer.data.get(
                    'username'), password=serializer.data.get('password'))
            except Exception as e:
                return Response({'error': f'Failed to register user: {str(e)}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response('succesfully registered', status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], serializer_class=UserLoginSerializer)
    def login(self, request):
        # Обработка запроса на авторизацию пользователя
            username = request.POST.get('username')
            password = request.POST.get('password')
            # Аутентификация пользователя
            user = authenticate(username=username, password=password)
            if user:
                # Генерация JWT-токена
                payload = {
                    'user_id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                    'iat': datetime.datetime.utcnow(),
                }
                jwt_token = jwt.encode(
                    payload, settings.SECRET_KEY, algorithm='HS256')
                # Возвращение токена в ответе
                return Response({'token': jwt_token})
            else:
                return Response({'error': 'Invalid credentials'})

    def list(self, request):
        queryset = User.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.filter(
            id=pk)
        user = queryset.first()
        if not user:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        if not request.user.is_superuser and request.user.id != pk:
            return Response({'detail': 'You do not have permission to perform this action.'},
                            status=status.HTTP_403_FORBIDDEN)
        queryset = User.objects.all()
        user = queryset.filter(id=pk).first()
        if not user:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(self.serializer_class(user).data)

    def destroy(self, request, pk=None):
        if not request.user.is_superuser and request.user.id != pk:
            return Response({'detail': 'You do not have permission to perform this action.'},
                            status=status.HTTP_403_FORBIDDEN)
        queryset = User.objects.all()
        user = queryset.filter(id=pk).first()
        if not user:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
