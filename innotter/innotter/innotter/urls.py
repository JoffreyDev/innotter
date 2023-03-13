from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from entities.views import PageViewSet, PostViewSet

router = DefaultRouter()

router.register(r'users',UserViewSet, basename='users')
router.register(r'pages',PageViewSet, basename='pages')
router.register(r'posts',PostViewSet, basename='posts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
