from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return True
