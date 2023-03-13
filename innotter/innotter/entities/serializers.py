from rest_framework import serializers
from .models import Page, Post, Tag

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'image', 'is_private', 'tags')

class PageCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('name', 'uuid', 'description', 'image', 'is_private', 'tags')

class PageFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('uuid', )

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user in instance.follow_requests.all():
            raise serializers.ValidationError("You already requested to follow this page")
        if user in instance.followers.all():
           raise serializers.ValidationError("You are in followers already")
        if instance.is_private:
            instance.follow_requests.add(user)
            validated_data['response'] = 'request sent'
            return validated_data
        instance.followers.add(user)
        validated_data['response'] = 'followed'
        return validated_data


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

