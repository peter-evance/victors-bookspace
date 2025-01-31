from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import *
from users.permissions import *
from users.serializers import *


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to custom user accounts.

    Provides CRUD functionality for custom user accounts.

    - list: Get a list of all custom users.
    - retrieve: Retrieve details of a specific custom user.
    - create: Create a new custom user account.
    - update: Update an existing custom user account.
    - destroy: Delete an existing custom user account.

    Serializer class used for request/response data depends on the action:
    - CustomUserCreateSerializer for create action.
    - CustomUserSerializer for other actions.

    """
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        return CustomUserSerializer
    

class AssignBookspaceOwnerView(APIView):
    """
    API View to assign the bookspace owner role to selected users.

    Only authenticated users with bookspace owner permission can access this view.

    The view accepts a POST request with a list of user IDs in the request body
    and assigns the bookspace owner role to the corresponding users.

    If successful, it returns a response with a message indicating the users
    who have been assigned the bookspace owner role. If any user ID is not found or
    is invalid, appropriate error messages are returned in the response.

    """
    permission_classes = [IsBookspaceOwner]

    def post(self, request):
        user_ids = request.data.getlist('user_ids', [])
        current_user_id = request.user.id

        assigned_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot assign roles to yourself.")

                user.assign_bookspace_owner()
                assigned_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if assigned_users:
            if len(assigned_users) > 1:
                response_data['message'] = f"Users {', '.join(assigned_users)} have been assigned as bookspace owners."
            else:
                response_data['message'] = f"User {assigned_users[0]} has been assigned as a bookspace owner."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data['error'] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data['error'] = f"User with ID '{not_found_ids[0]}' was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data['invalid'] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data['invalid'] = f"The ID '{invalid_ids[0]}' is invalid."

        return Response(response_data, status=status.HTTP_200_OK)


class AssignBookspaceManagerView(APIView):
    """
    API View to assign the bookspace manager role to selected users.

    Only authenticated users with bookspace owner permission can access this view.

    The view accepts a POST request with a list of user IDs in the request body
    and assigns the bookspace manager role to the corresponding users.

    If successful, it returns a response with a message indicating the users
    who have been assigned the bookspace manager role. If any user ID is not found
    or is invalid, appropriate error messages are returned in the response.

    """
    permission_classes = [IsBookspaceOwner]

    def post(self, request):
        user_ids = request.data.getlist('user_ids', [])
        current_user_id = request.user.id

        assigned_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot assign roles to yourself.")

                user.assign_bookspace_manager()
                assigned_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if assigned_users:
            if len(assigned_users) > 1:
                response_data['message'] = f"Users {', '.join(assigned_users)} have been assigned as bookspace managers."
            else:
                response_data['message'] = f"User {assigned_users[0]} has been assigned as a bookspace manager."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data['error'] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data['error'] = f"User with ID '{not_found_ids[0]}' was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data['invalid'] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data['invalid'] = f"The ID '{invalid_ids[0]}' is invalid."

        return Response(response_data, status=status.HTTP_200_OK)


class AssignAssistantBookspaceManagerView(APIView):
    """
    API View to assign the assistant bookspace manager role to selected users.

    Only authenticated users with bookspace owner permission can access this view.

    The view accepts a POST request with a list of user IDs in the request body
    and assigns the assistant bookspace manager role to the corresponding users.

    If successful, it returns a response with a message indicating the users
    who have been assigned the assistant bookspace manager role. If any user ID is not found
    or is invalid, appropriate error messages are returned in the response.

    """
    permission_classes = [IsBookspaceOwner]

    def post(self, request):
        user_ids = request.data.getlist('user_ids', [])
        current_user_id = request.user.id

        assigned_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot assign roles to yourself.")

                user.assign_assistant_bookspace_manager()
                assigned_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if assigned_users:
            if len(assigned_users) > 1:
                response_data['message'] = f"Users {', '.join(assigned_users)} have been assigned as assistant bookspace managers."
            else:
                response_data['message'] = f"User {assigned_users[0]} has been assigned as an assistant bookspace manager."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data['error'] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data['error'] = f"User with ID {not_found_ids[0]} was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data['invalid'] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data['invalid'] = f"The ID {invalid_ids[0]} is invalid."

        return Response(response_data, status=status.HTTP_200_OK)


class AssignBookspaceWorkerView(APIView):
    """
    API View to assign the bookspace worker role to selected users.

    Only authenticated users with bookspace manager permission can access this view.

    The view accepts a POST request with a list of user IDs in the request body
    and assigns the bookspace worker role to the corresponding users.

    If successful, it returns a response with a message indicating the users
    who have been assigned the bookspace worker role. If any user ID is not found
    or is invalid, appropriate error messages are returned in the response.

    """
    permission_classes = [IsBookspaceManager]

    def post(self, request):
        user_ids = request.data.getlist('user_ids', [])
        current_user_id = request.user.id

        assigned_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot assign roles to yourself.")

                user.assign_bookspace_worker()
                assigned_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if assigned_users:
            if len(assigned_users) > 1:
                response_data['message'] = f"Users {', '.join(assigned_users)} have been assigned as bookspace workers."
            else:
                response_data['message'] = f"User {assigned_users[0]} has been assigned as a bookspace worker."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data['error'] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data['error'] = f"User with ID {not_found_ids[0]} was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data['invalid'] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data['invalid'] = f"The ID {invalid_ids[0]} is invalid."

        return Response(response_data, status=status.HTTP_200_OK)


class DismissBookspaceManagerView(APIView):
    """
    API View to dismiss the bookspace manager role from selected users.

    Only authenticated users with bookspace owner permission can access this view.

    The view accepts a POST request with a list of user IDs in the request body
    and dismisses the bookspace manager role from the corresponding users.

    If successful, it returns a response with a message indicating the users
    who have been dismissed from the bookspace manager role. If any user ID is not found
    or is invalid, appropriate error messages are returned in the response.

    """
    permission_classes = [IsBookspaceOwner]

    def post(self, request):
        user_ids = request.data.getlist("user_ids", [])
        current_user_id = request.user.id

        dismissed_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot dismiss yourself.")

                user.dismiss_bookspace_manager()
                dismissed_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if dismissed_users:
            if len(dismissed_users) > 1:
                response_data[
                    "message"
                ] = f"Users {', '.join(dismissed_users)} have been dismissed as bookspace managers."
            else:
                response_data[
                    "message"
                ] = f"User {dismissed_users[0]} has been dismissed as a bookspace manager."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data[
                    "error"
                ] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data[
                    "error"
                ] = f"User with ID '{not_found_ids[0]}' was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data[
                    "invalid"
                ] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data["invalid"] = f"The ID '{invalid_ids[0]}' is invalid."

        return Response(response_data, status=status.HTTP_200_OK)


class DismissAssistantBookspaceManagerView(APIView):
    """
    API View to dismiss the assistant bookspace manager role from selected users.

    Only authenticated users with bookspace owner permission can access this view.

    The view accepts a POST request with a list of user IDs in the request body
    and dismisses the assistant bookspace manager role from the corresponding users.

    If successful, it returns a response with a message indicating the users
    who have been dismissed from the assistant bookspace manager role. If any user ID is not found
    or is invalid, appropriate error messages are returned in the response.

    """
    permission_classes = [IsBookspaceOwner]

    def post(self, request):
        user_ids = request.data.getlist("user_ids", [])
        current_user_id = request.user.id

        dismissed_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot dismiss yourself.")

                user.dismiss_assistant_bookspace_manager()
                dismissed_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if dismissed_users:
            if len(dismissed_users) > 1:
                response_data[
                    "message"
                ] = f"Users {', '.join(dismissed_users)} have been dismissed as assistant bookspace managers."
            else:
                response_data[
                    "message"
                ] = f"User {dismissed_users[0]} has been dismissed as an assistant bookspace manager."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data[
                    "error"
                ] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data[
                    "error"
                ] = f"User with ID {not_found_ids[0]} was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data[
                    "invalid"
                ] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data["invalid"] = f"The ID {invalid_ids[0]} is invalid."

        return Response(response_data, status=status.HTTP_200_OK)


class DismissBookspaceWorkerView(APIView):
    """
    API View to dismiss the bookspace worker role from selected users.

    Only authenticated users with bookspace manager permission can access this view.

    The view accepts a POST request with a list of user IDs in the request body
    and dismisses the bookspace worker role from the corresponding users.

    If successful, it returns a response with a message indicating the users
    who have been dismissed from the bookspace worker role. If any user ID is not found
    or is invalid, appropriate error messages are returned in the response.

    """

    permission_classes = [IsBookspaceManager]

    def post(self, request):
        user_ids = request.data.getlist("user_ids", [])
        current_user_id = request.user.id

        dismissed_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot dismiss yourself.")

                user.dismiss_bookspace_worker()
                dismissed_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if dismissed_users:
            if len(dismissed_users) > 1:
                response_data[
                    "message"
                ] = f"Users {', '.join(dismissed_users)} have been dismissed as bookspace workers."
            else:
                response_data[
                    "message"
                ] = f"User {dismissed_users[0]} has been dismissed as a bookspace worker."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data[
                    "error"
                ] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data[
                    "error"
                ] = f"User with ID {not_found_ids[0]} was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data[
                    "invalid"
                ] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data["invalid"] = f"The ID {invalid_ids[0]} is invalid."

        return Response(response_data, status=status.HTTP_200_OK)


class GenerateUsernameSlugAPIView(APIView):
    """
    API View to generate a unique username slug based on first name and last name.

    This view accepts a POST request with the `first_name` and `last_name` fields in the request body.
    It generates a username slug by concatenating the sanitized `first_name` and `last_name` strings
    and returns it as a response.

    The generated username slug is unique and can be used to create a new user with a username based
    on their first name and last name. If the `first_name` or `last_name` is not provided in the request
    body, it returns an error response with a message indicating that both fields are required.

    Example usage:
    POST /users/generate-username/
    Request Body:
    {
        "first_name": "Peter",
        "last_name": "Evance"
    }

    Response:
    {
        "username": "peter-evance"
    }
    """

    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if not first_name:
            return Response({'error': 'First name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not last_name:
            return Response({'error': 'Last name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        username = CustomUser.generate_username(first_name, last_name)

        return Response({'username': username})
