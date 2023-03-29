from rest_framework import serializers
from .models import Page, Post, Tag
from users.models import User

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'image', 'is_private', 'tags')

class PageCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('name', 'uuid', 'description', 'image', 'is_private', 'tags')


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', )


class PageSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('uuid', )

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user == instance.owner:
            raise serializers.ValidationError("You are an owner of the page")
        if user in instance.follow_requests.all():
            raise serializers.ValidationError("You already requested to follow this page")
        if user in instance.followers.all():
           raise serializers.ValidationError("You are in followers already")
        if instance.is_private:
            instance.follow_requests.add(user)
            validated_data['response'] = 'Request sent'
            return validated_data
        instance.followers.add(user)
        validated_data['response'] = 'Followed'
        return validated_data
    
class PageListSubscribeRequestSerializer(serializers.ModelSerializer):
    follow_requests = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ('follow_requests', )

    def get_follow_requests(self, obj):
        return FollowerSerializer(obj.follow_requests.all(), many=True).data

    
class PageChangeSubscribeRequestStatus(serializers.ModelSerializer):
    action = serializers.CharField(write_only=True)
    follower_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Page
        fields = ('uuid', 'action', 'follower_id')

    def update(self, instance, validated_data):
        user = self.context['request'].user
        follower_instance = User.objects.get(pk=validated_data.get('follower_id'))
        action = validated_data.get('action')
        if not follower_instance in instance.follow_requests.all():
            validated_data['response'] = 'Follow request not found'
            return validated_data
        if action == 'accept':
            instance.follow_requests.remove(user)
            instance.followers.add(user)
            validated_data['response'] = 'Follow request accepted'
            return validated_data
        if action == 'reject':
            instance.follow_requests.remove(user)
            validated_data['response'] = 'Follow request rejected'
            return validated_data
        
class PageChangeAllSubscribeRequestsStatuses(serializers.ModelSerializer):
    action = serializers.CharField(write_only=True)

    class Meta:
        model = Page
        fields = ('action', )

    def update(self, instance, validated_data):
        action = validated_data.get('action')
        if instance.follow_requests.all().count() < 1:
            validated_data['response'] = 'No requests found'
            return validated_data
        if action == 'accept':
            for user in instance.follow_requests.all():
                instance.follow_requests.remove(user)
                instance.followers.add(user)
            validated_data['response'] = 'All follow requests accepted'
            return validated_data
        if action == 'reject':
            for user in instance.follow_requests.all():
                instance.follow_requests.remove(user)
            validated_data['response'] = 'All follow requests rejected'
            return validated_data


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('page', 'content', 'reply_to', 'id')

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('content', 'reply_to', 'page')

    def create(self, validated_data):
        user = self.context['request'].user
        page = validated_data.get('page')
        if not page.owner == user:
            raise serializers.ValidationError("You haven`t permissions to post on this page")
        post = Post.objects.create(content=validated_data.get('content'), reply_to=validated_data.get('reply_to') if validated_data.get('reply_to') else None, page=page)
        return post
    
class PostAddLikeSerializer(serializers.ModelSerializer):
    post = serializers.IntegerField()
    class Meta:
        model = Post
        fields = ('post', )

    def update(self, instance, validated_data):
            user = self.context['request'].user
            instance.likes.add(user)
            validated_data['response'] = 'Post liked'
            return validated_data
        
class PostRemoveLikeSerializer(serializers.ModelSerializer):
    post = serializers.IntegerField()
    class Meta:
        model = Post
        fields = ('post', )

    def update(self, instance, validated_data):
            user = self.context['request'].user
            instance.likes.remove(user)
            validated_data['response'] = 'Like removed'
            return validated_data
          
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        

