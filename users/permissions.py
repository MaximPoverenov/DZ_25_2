from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsModerator(permissions.BasePermission):
    """
    Позволяет доступ только модераторам.
    """

    def has_permission(self, request, view):
        # Проверяем, что пользователь в группе "Moderators"
        return request.user.groups.filter(name="Moderators").exists()

    def has_object_permission(self, request, view, obj):
        # Модераторам разрешено только чтение и изменение объектов
        if view.action in ["list", "retrieve", "update", "partial_update"]:
            return True
        return False


class IsOwner(BasePermission):
    """
    Проверяет, является ли пользователь владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user