from django.shortcuts import render
from .serializers import PageSerializer, PostSerializer, PageCreateSerializer
from rest_framework import viewsets
from .models import Page, Post
from rest_framework.response import Response
from innotter.permissions import IsPageOwnerOrAdminModer
from rest_framework.decorators import action

class PageViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for viewing and editing Page.
    """

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'update':
            permission_classes = [IsPageOwnerOrAdminModer]
        else:
            permission_classes = [IsPageOwnerOrAdminModer]
        return [permission() for permission in permission_classes]

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create' or self.action == 'update':
            return PageCreateSerializer(*args, **kwargs)
        return PageSerializer(*args, **kwargs)
    
    def list(self, request):
        self.check_permissions(request)
        queryset = Page.objects.all()
        serializer = PageSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PageCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        try:
            page = Page.objects.get(pk=pk)
            self.check_object_permissions(request, page)
        except Page.DoesNotExist:
            return Response(status=404)

        serializer = PageSerializer(page)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            page = Page.objects.get(pk=pk)
            self.check_object_permissions(request, page)
        except Page.DoesNotExist:
            return Response(status=404)

        serializer = PageSerializer(page, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            page = Page.objects.get(pk=pk)
            self.check_object_permissions(request, page)
        except Page.DoesNotExist:
            return Response(status=404)

        page.delete()
        return Response(status=204)
    
class PostViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for viewing and editing Posts.
    """
    serializer_class = PostSerializer

    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=404)

        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=404)

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=404)

        post.delete()
        return Response(status=204)
    
    

