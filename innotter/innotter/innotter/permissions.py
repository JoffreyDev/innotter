from rest_framework import permissions
from entities.models import Page


class IsPageOwnerOrAdminModer(permissions.BasePermission):
    """
    Права изменения, редактирования, удаления, просмотра страниц пользователем
    """

    def has_permission(self, request, view):
        return request.user.role == 'moderator' or request.user.role == 'admin' if request.user.is_authenticated else False

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user.role == 'moderator' or request.user.role == 'admin' if request.user.is_authenticated else False
    
class IsPostOwnerOrAdminModer(permissions.BasePermission):
    """
    Права на редактирование, удаление поста со страницы
    """

    def has_permission(self, request, view):
        return request.user.role == 'moderator' or request.user.role == 'admin' if request.user.is_authenticated else False

    def has_object_permission(self, request, view, obj):
        page = obj.page
        owner = page.owner
        return request.user == owner or request.user.role == 'moderator' or request.user.role == 'admin' if request.user.is_authenticated else False
    
    
