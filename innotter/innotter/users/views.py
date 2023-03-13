from users.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
    