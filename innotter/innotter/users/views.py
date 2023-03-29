from users.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from rest_framework.decorators import action
from entities.models import Post, Page
from django.db.models import Q
from entities.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
import json
import pika
from services.statistics_service import get_user_statistics_from_microservice

from django.http import JsonResponse
from django.conf import settings


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()


    permission_classes_by_action = {
        'create': [],
        'list': [],
        'login': [],
        'register': [],
        'retrieve': [IsAuthenticated],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
        'destroy': [IsAuthenticated],
        'liked_posts_list': [IsAuthenticated],
        'get_statistics': [IsAuthenticated],
        'news': [IsAuthenticated],
    }

    serializer_classes_by_action = {
        'list': UserSerializer,
        'login': UserLoginSerializer,
        'register': UserRegisterSerializer,
        'retrieve': UserSerializer,
        'update': UserSerializer,
        'partial_update': UserSerializer,
        'destroy': UserSerializer,
        'liked_posts_list': PostSerializer,
        'news': PostSerializer,
    }

      # Getting permissions for specific action
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    # Getting serializer for specific action
    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, UserSerializer)

    @action(detail=False, methods=['post'], serializer_class=UserRegisterSerializer)
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid()
        try:
            serializer.save()
        except Exception as e:
            return Response({'error': f'Failed to register user: {str(e)}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('succesfully registered', status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], serializer_class=UserLoginSerializer)
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'token': serializer.validated_data['token']})
    
    @action(detail=False, methods=['get'], serializer_class=PostSerializer)
    def liked_posts_list(self, request):
        user = request.user
        queryset = Post.objects.filter(Q(likes=user))
        serializer = PostSerializer(queryset, many=True)
        return Response({'posts': serializer.data})
    
    @action(detail=False, methods=['get'])
    def get_statistics(self, request):
    # Подготавливаем данные для отправки на микросервис
        data = {
            'user_id': request.user.id,
        }
        message = json.dumps(data)

        # Устанавливаем соединение с RabbitMQ
        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, settings.RABBITMQ_VIRTUAL_HOST, credentials))
        channel = connection.channel()

        # Отправляем сообщение на очередь RabbitMQ
        channel.basic_publish(exchange='', routing_key=settings.RABBITMQ_STATISTICS_QUEUE, body=message)

        # Получаем ответ от микросервиса
        method_frame, header_frame, body = channel.basic_get(queue='user_statistics')
        if method_frame:
            response = json.loads(body.decode())
            channel.basic_ack(method_frame.delivery_tag)
            connection.close()
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'No response from statistics microservice'})
        
    @action(detail=False, methods=['get'], serializer_class=PostSerializer)
    def news(self, request):
        user = request.user
        pages = Page.objects.filter(owner=user) | Page.objects.filter(followers=user)
        posts = Post.objects.filter(page__in=pages)
        posts = posts.order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response({'posts': serializer.data})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        user_id = request.user.id
        response = get_user_statistics_from_microservice(user_id)
        return Response(response)
    
    