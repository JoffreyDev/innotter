from rest_framework import serializers
from users.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password',]
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'