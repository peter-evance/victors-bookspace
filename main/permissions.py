from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.permissions import BasePermission


class CanActOnAuthor(BasePermission):
    message = {"message": "Only bookspace owners, managers, and assistants have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is an assistant bookspace manager
        if request.user.is_authenticated and (
                request.user.is_assistant_bookspace_manager or request.user.is_bookspace_manager
                or request.user.is_bookspace_owner):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanActOnBookTag(BasePermission):
    message = {"message": "Only bookspace owners, managers, and assistants have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is an assistant bookspace manager
        if request.user.is_authenticated and (
                request.user.is_assistant_bookspace_manager or request.user.is_bookspace_manager
                or request.user.is_bookspace_owner):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanAddBook(BasePermission):
    message = {"message": "Only bookspace staff and workers have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a bookspace worker
        if request.user.is_authenticated and (request.user.is_bookspace_owner or request.user.is_bookspace_worker or
                                              request.user.is_bookspace_manager or request.user.is_assistant_bookspace_manager):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanDeleteBook(BasePermission):
    message = {"message": "Only bookspace owner and managers have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is an assistant bookspace manager as well as others
        if request.user.is_authenticated and (request.user.is_bookspace_manager or request.user.is_bookspace_owner):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanUpdateBook(BasePermission):
    message = {"message": "Only bookspace owners, managers, and assistants have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is an assistant bookspace manager as well as others
        if request.user.is_authenticated and (
                request.user.is_assistant_bookspace_manager or request.user.is_bookspace_manager
                or request.user.is_bookspace_owner):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanAddBookImage(BasePermission):
    message = {"message": "Only bookspace staff and workers have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a bookspace worker
        if request.user.is_authenticated and (request.user.is_bookspace_owner or request.user.is_bookspace_worker or
                                              request.user.is_bookspace_manager or request.user.is_assistant_bookspace_manager):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanDeleteBookImage(BasePermission):
    message = {"message": "Only bookspace owner and managers have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is an assistant bookspace manager as well as others
        if request.user.is_authenticated and (request.user.is_bookspace_manager or request.user.is_bookspace_owner):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanUpdateBookImage(BasePermission):
    message = {"message": "Only bookspace owners, managers, and assistants have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is an assistant bookspace manager as well as others
        if request.user.is_authenticated and (
                request.user.is_assistant_bookspace_manager or request.user.is_bookspace_manager
                or request.user.is_bookspace_owner):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)
