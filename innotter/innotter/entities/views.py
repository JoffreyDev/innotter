from django.shortcuts import render
from .serializers import PageSerializer, PostSerializer, PageCreateUpdateSerializer, PageFollowSerializer
from rest_framework import viewsets
from .models import Page, Post
from rest_framework.response import Response
from innotter.permissions import IsOwnerOrAdminModer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class PageViewSet(viewsets.ModelViewSet):

    permission_classes = [IsOwnerOrAdminModer]

    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'retrieve': [IsOwnerOrAdminModer],
        'update': [IsOwnerOrAdminModer],
        'partial_update': [IsOwnerOrAdminModer],
        'destroy': [IsOwnerOrAdminModer],
        'subscribe_to_page': [IsAuthenticated],
    }

    serializer_classes_by_action = {
        'list': PageSerializer,
        'create': PageCreateUpdateSerializer,
        'retrieve': PageSerializer,
        'update': PageCreateUpdateSerializer,
        'partial_update': PageCreateUpdateSerializer,
        'destroy': PageSerializer,
        'subscribe_to_page': PageFollowSerializer,
    }

    queryset = Page.objects.all()

    # Getting permissions for specific action
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    # Getting serializer for specific action
    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, PageSerializer)
    
    @action(detail=False, methods=['post'], serializer_class = PageFollowSerializer)
    def subscribe_to_page(self, request):
        instance = get_object_or_404(Page, uuid=request.data.get('uuid'))
        serializer = PageFollowSerializer(instance=instance, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, validated_data=serializer.validated_data)
        return Response(serializer.validated_data.get('response'))


class PostViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Posts.
    """

    permission_classes = [IsOwnerOrAdminModer]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
