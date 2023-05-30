from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return True


class AuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method == 'get' or request.user == obj.author)
