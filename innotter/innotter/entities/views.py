from django.shortcuts import render
from .serializers import PageSerializer, PostSerializer, PageCreateUpdateSerializer, PageSubscribeSerializer, \
    PageChangeSubscribeRequestStatus, PageListSubscribeRequestSerializer, PageChangeAllSubscribeRequestsStatuses, PostCreateSerializer, \
    PostAddLikeSerializer, PostRemoveLikeSerializer
from rest_framework import viewsets
from .models import Page, Post
from rest_framework.response import Response
from innotter.permissions import IsPageOwnerOrAdminModer, IsPostOwnerOrAdminModer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class PageViewSet(viewsets.ModelViewSet):

    permission_classes = [IsPageOwnerOrAdminModer]

    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'retrieve': [IsPageOwnerOrAdminModer],
        'update': [IsPageOwnerOrAdminModer],
        'partial_update': [IsPageOwnerOrAdminModer],
        'destroy': [IsPageOwnerOrAdminModer],
        'subscribe_to_page': [IsAuthenticated],
        'change_subscribe_request_status': [IsPageOwnerOrAdminModer],
        'list_subscribe_requests': [IsPageOwnerOrAdminModer],
        'change_all_subscribe_requests_statuses': [IsPageOwnerOrAdminModer],
    }

    serializer_classes_by_action = {
        'list': PageSerializer,
        'create': PageCreateUpdateSerializer,
        'retrieve': PageSerializer,
        'update': PageCreateUpdateSerializer,
        'partial_update': PageCreateUpdateSerializer,
        'destroy': PageSerializer,
        'subscribe_to_page': PageSubscribeSerializer,
        'change_subscribe_request_status': PageChangeSubscribeRequestStatus,
        'list_subscribe_requests': PageListSubscribeRequestSerializer,
        'change_all_subscribe_requests_statuses': PageChangeAllSubscribeRequestsStatuses,
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

    @action(detail=False, methods=['post'], serializer_class=PageSubscribeSerializer)
    def subscribe_to_page(self, request):
        instance = get_object_or_404(Page, uuid=request.data.get('uuid'))
        serializer = PageSubscribeSerializer(
            instance=instance, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, validated_data=serializer.validated_data)
        return Response(serializer.validated_data.get('response'))

    @action(detail=True, methods=['get'], serializer_class=PageListSubscribeRequestSerializer)
    def list_subscribe_requests(self, request, pk=None):
        instance = get_object_or_404(Page, id=pk)
        self.check_object_permissions(request, instance)
        serializer = PageListSubscribeRequestSerializer(instance=instance)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], serializer_class=PageChangeSubscribeRequestStatus)
    def change_subscribe_request_status(self, request):
        instance = get_object_or_404(Page, uuid=request.data.get('uuid'))
        self.check_object_permissions(request, instance)
        serializer = PageChangeSubscribeRequestStatus(
            instance=instance, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, validated_data=serializer.validated_data)
        return Response(serializer.validated_data.get('response'))
    
    @action(detail=True, methods=['post'], serializer_class=PageChangeAllSubscribeRequestsStatuses)
    def change_all_subscribe_requests_statuses(self, request, pk=None):
        instance = get_object_or_404(Page, id=pk)
        self.check_object_permissions(request, instance)
        serializer = PageChangeAllSubscribeRequestsStatuses(
            instance=instance, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, validated_data=serializer.validated_data)
        return Response(serializer.validated_data.get('response'))


class PostViewSet(viewsets.ModelViewSet):

    permission_classes = [IsPostOwnerOrAdminModer]

    permission_classes_by_action = {
        'create': [],
        'list': [],
        'retrieve': [IsAuthenticated],
        'update': [IsPostOwnerOrAdminModer],
        'partial_update': [IsPostOwnerOrAdminModer],
        'destroy': [IsPostOwnerOrAdminModer],
        'like': [IsAuthenticated],
        'unlike': [IsAuthenticated],
    }

    serializer_classes_by_action = {
        'list': PostSerializer,
        'create': PostCreateSerializer,
        'retrieve': PostSerializer,
        'update': PostSerializer,
        'partial_update': PostSerializer,
        'destroy': PostSerializer,
        'like': PostAddLikeSerializer,
        'unlike': PostRemoveLikeSerializer,
    }

    queryset = Post.objects.all()
    serializer_class = PostSerializer

     # Getting permissions for specific action
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    # Getting serializer for specific action
    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, PageSerializer)
    
    @action(detail=False, methods=['post'], serializer_class=PostAddLikeSerializer)
    def like(self, request):
        post = get_object_or_404(Post, pk=request.data['post'])
        serializer = PostAddLikeSerializer(data = request.data, context={'request': request}, instance=post)
        serializer.is_valid(raise_exception=True)
        serializer.update(post, validated_data=serializer.validated_data)
        return Response(serializer.validated_data.get('response'))
    
    @action(detail=False, methods=['post'], serializer_class=PostRemoveLikeSerializer)
    def unlike(self, request):
        post = get_object_or_404(Post, pk=request.data.get('post'))
        serializer = PostRemoveLikeSerializer(data = request.data, context={'request': request}, instance=post)
        serializer.is_valid(raise_exception=True)
        serializer.update(post, serializer.validated_data)
        return Response(serializer.validated_data.get('response'))
    
    