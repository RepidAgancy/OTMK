from rest_framework.permissions import BasePermission

from account import models


class IsLeader(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == models.LEADER:
                return True
        else:
            return False


class IsProgrammer(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == models.PROGRAMMER:
                return True
        else:
            return False


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == models.EMPLOYEE:
                return True
        else:
            return False
