from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает доступ к объекту только владельцу.
    """

    def has_object_permission(self, request, view, obj):
        # Все могут читать (GET), но только владелец может изменять (PUT, PATCH, DELETE)
        if request.method in ("GET",):
            return True
        return (
            obj.owner == request.user
        )  # Проверка, что пользователь — владелец объекта