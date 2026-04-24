from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return True


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return True
