from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsBookspaceOwner(BasePermission):
    """
    Custom permission class that allows only bookspace owners to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a bookspace owner.

    Usage:
        Add the permission class to the view or viewset that requires bookspace owners access:
        permission_classes = [IsBookspaceOwner]
    """

    message = {"message": "Only bookspace owners have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a bookspace owner
        if request.user.is_authenticated and request.user.is_bookspace_owner:
            return True
        raise PermissionDenied(self.message)


class IsBookspaceManager(BasePermission):
    """
    Custom permission class that allows only bookspace owners and managers to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a bookspace owner or a bookspace manager.

    Usage:
        Add the permission class to the view or viewset that requires bookspace owners and managers access:
        permission_classes = [IsBookspaceManager]
    """
    message = {"message": "Only bookspace owners and managers have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a bookspace manager
        if request.user.is_authenticated and (request.user.is_bookspace_manager or request.user.is_bookspace_owner):
            return True
        raise PermissionDenied(self.message)


class IsAssistantBookspaceManager(BasePermission):
    """
    Custom permission class that allows only bookspace owners, managers, and assistants to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a bookspace owner, a bookspace manager, or an assistant bookspace manager.

    Usage:
        Add the permission class to the view or viewset that requires bookspace owners, managers, and assistants access:
        permission_classes = [IsAssistantBookspaceManager]
    """
    message = {"message": "Only bookspace owners, managers, and assistants have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is an assistant bookspace manager
        if request.user.is_authenticated and (
                request.user.is_assistant_bookspace_manager or request.user.is_bookspace_manager
                or request.user.is_bookspace_owner):
            return True
        raise PermissionDenied(self.message)


class IsBookspaceWorker(BasePermission):
    """
    Custom permission class that allows only bookspace staff and workers to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a bookspace owner, a bookspace worker, a bookspace manager, or an assistant bookspace manager.

    Usage:
        Add the permission class to the view or viewset that requires bookspace workers access:
        permission_classes = [IsBookspaceWorker]
    """
    message = {"message": "Only bookspace staff and workers have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a bookspace worker
        if request.user.is_authenticated and (request.user.is_bookspace_owner or request.user.is_bookspace_worker or
                                              request.user.is_bookspace_manager or request.user.is_assistant_bookspace_manager):
            return True
        raise PermissionDenied(self.message)
