from rest_framework import serializers
from .models import Page, Post, Tag

class PageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('name', 'uuid', 'description', 'image', 'is_private',)


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'