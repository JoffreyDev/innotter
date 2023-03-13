from rest_framework import permissions

class IsPageOwnerOrAdminModer(permissions.BasePermission):
    """
    Пользователь может просмотреть страницу только если он является ее владельцем или
    админом/модератором
    """

    def has_permission(self, request, view):
        return request.user.role == 'moderator' or request.user.role == 'admin' if request.user.is_authenticated else False
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner