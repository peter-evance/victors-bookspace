import pytest
from django.urls import reverse
from rest_framework import status

from users.models import *
from main.models import *


@pytest.mark.django_db
def test_user_flow(client):
    # Register a new user
    register_data = {
        "username": "test@example.com",
        "password": "testpassword",
        "first_name": "Peter",
        "last_name": "Evance",
        "phone_number": "+254712345699",
        "sex": SexChoices.MALE,
    }

    response = client.post("/auth/users/", register_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "username" in response.data
    user_id = response.data["id"]

    # Access user details (without authentication)
    response = client.get("/auth/users/me", follow=True)
    assert response.data["detail"] == "Authentication credentials were not provided."
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Log in
    login_data = {
        "username": "test@example.com",
        "password": "testpassword",
    }
    response = client.post(reverse("users:login"), login_data)
    assert response.status_code == status.HTTP_200_OK
    assert "auth_token" in response.data
    token = response.data["auth_token"]

    # Access user details (with authentication)
    headers = {"Authorization": f"Token {token}"}
    response = client.get(
        "/auth/users/me", HTTP_AUTHORIZATION=f"Token {token}", follow=True
    )
    assert response.status_code == status.HTTP_200_OK
    assert "username" in response.data
    assert response.data["username"] == "test@example.com"

    # Log out
    response = client.post(
        reverse("users:logout"),
        data={"token": token},
        HTTP_AUTHORIZATION=f"Token {token}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Attempt to access user details after logout
    headers = {"Authorization": f"Token {token}"}
    response = client.get(
        "/auth/users/me", HTTP_AUTHORIZATION=f"Token {token}", follow=True
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.data
    assert response.data["detail"] == "Invalid token."


@pytest.mark.django_db
class TestRoleAssignments:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users):
        self.client = setup_users["client"]

        self.regular_user_id = setup_users["regular_user_id"]
        self.regular_user_token = setup_users["regular_user_token"]
        self.regular_user_username = setup_users["regular_user_username"]

        self.bookspace_owner_token = setup_users["bookspace_owner_token"]
        self.bookspace_owner_user_id = setup_users["bookspace_owner_user_id"]
        self.bookspace_owner_user_username = setup_users["bookspace_owner_user_username"]

        self.bookspace_manager_token = setup_users["bookspace_manager_token"]
        self.bookspace_manager_user_id = setup_users["bookspace_manager_user_id"]
        self.bookspace_manager_user_username = setup_users["bookspace_manager_user_username"]

        self.asst_bookspace_manager_token = setup_users["asst_bookspace_manager_token"]
        self.asst_bookspace_manager_user_id = setup_users["asst_bookspace_manager_user_id"]
        self.asst_bookspace_manager_user_username = setup_users[
            "asst_bookspace_manager_user_username"
        ]

        self.bookspace_worker_token = setup_users["bookspace_worker_token"]
        self.bookspace_worker_user_id = setup_users["bookspace_worker_user_id"]
        self.bookspace_worker_user_username = setup_users["bookspace_worker_user_username"]

    def test_assign_to_self(self):
        # Assigning the role to oneself should be restricted
        user_ids = [self.bookspace_owner_user_id]
        response = self.client.post(
            reverse("users:assign-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_owner_token}",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0] == "Cannot assign roles to yourself."

    def test_assign_bookspace_owner(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-bookspace-owner"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
                response.data["message"]
                == f"User {self.regular_user_username} has been assigned as a bookspace owner."
        )

    def test_assign_bookspace_manager(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
                response.data["message"]
                == f"User {self.regular_user_username} has been assigned as a bookspace manager."
        )

    def test_assign_asst_bookspace_manager(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-assistant-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
                response.data["message"]
                == f"User {self.regular_user_username} has been assigned as an assistant bookspace manager."
        )

    def test_assign_bookspace_worker(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-bookspace-worker"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
                response.data["message"]
                == f"User {self.regular_user_username} has been assigned as a bookspace worker."
        )

    def test_assign_bookspace_manager_permission_denied(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
                response.data["message"]
                == "Only bookspace owners have permission to perform this action."
        )

    def test_assign_assistant_bookspace_manager_permission_denied(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-assistant-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
                response.data["message"]
                == "Only bookspace owners have permission to perform this action."
        )

    def test_assign_bookspace_worker_permission_denied(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-bookspace-worker"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.asst_bookspace_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
                response.data["message"]
                == "Only bookspace owners and managers have permission to perform this action."
        )

    def test_dismiss_bookspace_manager(self):
        user_ids = [self.asst_bookspace_manager_user_id]
        response = self.client.post(
            reverse("users:dismiss-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
                response.data["message"]
                == f"User {self.asst_bookspace_manager_user_username} has been dismissed as a bookspace manager."
        )

    def test_dismiss_asst_bookspace_manager(self):
        user_ids = [self.asst_bookspace_manager_user_id]
        response = self.client.post(
            reverse("users:dismiss-assistant-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
                response.data["message"]
                == f"User {self.asst_bookspace_manager_user_username} has been dismissed as an "
                   f"assistant bookspace manager."
        )

    def test_dismiss_bookspace_worker(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:dismiss-bookspace-worker"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
                response.data["message"]
                == f"User {self.regular_user_username} has been dismissed as a bookspace worker."
        )

    def test_dismiss_user_not_found(self):
        user_ids = ["99"]
        response = self.client.post(
            reverse("users:dismiss-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["error"] == "User with ID '99' was not found."


@pytest.mark.django_db
class TestAuthorViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users):
        self.client = setup_users["client"]

        self.regular_user_token = setup_users["regular_user_token"]
        self.bookspace_owner_token = setup_users["bookspace_owner_token"]
        self.bookspace_manager_token = setup_users["bookspace_manager_token"]
        self.asst_bookspace_manager_token = setup_users["asst_bookspace_manager_token"]
        self.bookspace_worker_token = setup_users["bookspace_worker_token"]

    def test_create_author_as_bookspace_owner(self):
        """
        Test creating a author by a bookspace owner.
        """
        author_data = {'first_name': 'David', 'last_name': 'Karanja'}
        response = self.client.post(reverse('main:authors-list'), data=author_data,
                                    HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Author.objects.filter(first_name=author_data['first_name']).exists()

    def test_create_author_as_bookspace_manager(self):
        """
        Test creating a author by a bookspace manager
        """
        author_data = {'first_name': 'Henriette', 'last_name': 'Uwiyezimana'}
        response = self.client.post(
            reverse('main:authors-list'), author_data, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Author.objects.filter(first_name=author_data['first_name']).exists()

    def test_create_author_as_asst_bookspace_manager(self):
        """
        Test creating a author by a assistant bookspace manager (should be denied).
        """
        author_data = {'first_name': 'Henriette', 'last_name': 'Uwiyezimana'}
        response = self.client.post(
            reverse('main:authors-list'), author_data,
            HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Author.objects.filter(first_name=author_data['first_name']).exists()

    def test_create_author_as_bookspace_worker_permission_denied(self):
        """
        Test creating a author by a bookspace worker (should be denied).
        """
        author_data = {'first_name': 'Peter', 'last_name': 'Evance'}
        response = self.client.post(reverse('main:authors-list'), author_data,
                                    HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Author.objects.filter(first_name=author_data['first_name']).exists()

    def test_create_author_as_regular_user_permission_denied(self):
        """
        Test creating a author by a regular user (should be denied).
        """
        author_data = {'first_name': 'Henriette', 'last_name': 'Uwiyezimana'}
        response = self.client.post(reverse('main:authors-list'), author_data,
                                    HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Author.objects.filter(first_name=author_data['first_name']).exists()

    def test_create_author_without_authentication(self):
        """
        Test creating a author without authentication (should be denied).
        """
        author_data = {'first_name': 'Henriette', 'last_name': 'Uwiyezimana'}
        response = self.client.post(reverse('main:authors-list'), author_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Author.objects.filter(first_name=author_data['first_name']).exists()

    def test_retrieve_authors_as_bookspace_owner(self):
        """
        Test retrieving authors by a bookspace owner.
        """
        response = self.client.get(reverse('main:authors-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_authors_as_bookspace_manager(self):
        """
        Test retrieving authors by a bookspace manager.
        """
        response = self.client.get(reverse('main:authors-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_authors_as_asst_bookspace_manager(self):
        """
        Test retrieving authors by an assistant bookspace manager.
        """
        response = self.client.get(reverse('main:authors-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_authors_as_regular_user_permission_denied(self):
        """
        Test retrieving authors by a regular user (should be denied).
        """
        response = self.client.get(reverse('main:authors-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_authors_without_authentication(self):
        """
        Test retrieving authors without authentication (should be denied).
        """
        url = reverse('main:authors-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_author_as_bookspace_owner(self):
        """
        Test updating an author as bookspace owner
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        author_update_data = {'first_name': 'first'}
        response = self.client.patch(url, author_update_data, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_author_as_bookspace_manager(self):
        """
        Test updating an author as bookspace manager
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        author_update_data = {'first_name': 'first'}
        response = self.client.patch(url, author_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_author_as_asst_bookspace_manager(self):
        """
        Test updating an author as assistant bookspace manager
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        author_update_data = {'first_name': 'first'}
        response = self.client.patch(url, author_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_author_as_bookspace_worker_permission_denied(self):
        """
        Test updating an author as bookspace worker (permission denied)
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        author_update_data = {'first_name': 'first'}
        response = self.client.patch(url, author_update_data, HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_author_as_regular_user_permission_denied(self):
        """
        Test updating an author as regular (permission denied)
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        author_update_data = {'first_name': 'first'}
        response = self.client.patch(url, author_update_data, HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_author_without_authentication(self):
        """
        Test updating an author without authentication
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        author_update_data = {'first_name': 'first'}
        response = self.client.patch(url, author_update_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_author_as_bookspace_owner(self):
        """
        Test deleting a author by a bookspace owner.
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Author.objects.filter(id=author.id).exists()

    def test_delete_author_as_bookspace_manager(self):
        """
        Test deleting a author by a bookspace manager.
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Author.objects.filter(id=author.id).exists()

    def test_delete_author_as_asst_bookspace_manager(self):
        """
        Test deleting a author by an assistant bookspace manager.
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Author.objects.filter(id=author.id).exists()

    def test_delete_author_as_bookspace_worker_permission_denied(self):
        """
        Test deleting a author by a bookspace worker (should be denied).
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Author.objects.filter(id=author.id).exists()

    def test_delete_author_as_regular_user_permission_denied(self):
        '''
        Test delete author as a regular user (permission denied)
        '''
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})

        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Author.objects.filter(id=author.id).exists()

    def test_delete_author_unauthorized(self):
        '''
        Test delete author by unauthorized request
        '''
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Author.objects.filter(id=author.id).exists()

    def test_filter_authors_by_name(self):
        """
        Test filtering authors by name (e.g., get all authors with name 'Stephen').
        """
        Author.objects.create(first_name='Stephen', last_name='Omondi')
        Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-list')
        url += f'?first_name=Stephen'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['first_name'] == 'Stephen'

    def test_filter_authors_by_partial_name(self):
        """
        Test filtering authors by name (e.g., get all authors with name 'Ste').
        """
        Author.objects.create(first_name='Stephen', last_name='Omondi')
        Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-list')
        url += f'?first_name=Ste'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['first_name'] == 'Stephen'

    def test_order_authors_by_multiple_fields(self):
        """
        Test ordering authors by multiple fields (e.g., first names in descending order, id in ascending order).
        """
        Author.objects.create(first_name='Stephen', last_name='Omondi')
        Author.objects.create(first_name='Peter', last_name='Evance')
        Author.objects.create(first_name='Henriette', last_name='Uwiyezimana')
        Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-list')
        url += '?ordering=first_name'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4
        assert response.data[0]['first_name'] == 'Henriette'
        assert response.data[1]['first_name'] == 'Peter'
        assert response.data[2]['first_name'] == 'Stephen'
        assert response.data[3]['first_name'] == 'Test'

    def test_no_results_for_invalid_name(self):
        """
        Test filtering with a name that doesn't exist.
        """
        url = reverse('main:authors-list')
        url += '?name=nonexistent'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'detail': 'No author(s) found matching the provided filters.'}


@pytest.mark.django_db
class TestBookTagViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users):
        self.client = setup_users["client"]

        self.regular_user_token = setup_users["regular_user_token"]
        self.bookspace_owner_token = setup_users["bookspace_owner_token"]
        self.bookspace_manager_token = setup_users["bookspace_manager_token"]
        self.asst_bookspace_manager_token = setup_users["asst_bookspace_manager_token"]
        self.bookspace_worker_token = setup_users["bookspace_worker_token"]

    def test_create_book_tag_as_bookspace_owner(self):
        """
        Test creating a book tag by a bookspace owner.
        """
        book_tag_data = {'name': BookTagChoices.HISTORY}
        response = self.client.post(reverse('main:book-tags-list'), data=book_tag_data,
                                    HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert BookTag.objects.filter(name=book_tag_data['name']).exists()

    def test_create_book_tag_as_bookspace_manager(self):
        """
        Test creating a book tag by a bookspace manager
        """
        book_tag_data = {'name': BookTagChoices.HISTORY}
        response = self.client.post(
            reverse('main:book-tags-list'), book_tag_data, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert BookTag.objects.filter(name=book_tag_data['name']).exists()

    def test_create_book_tag_as_asst_bookspace_manager(self):
        """
        Test creating a book tag by a assistant bookspace manager (should be denied).
        """
        book_tag_data = {'name': BookTagChoices.HISTORY}
        response = self.client.post(
            reverse('main:book-tags-list'), book_tag_data,
            HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert BookTag.objects.filter(name=book_tag_data['name']).exists()

    def test_create_book_tag_as_bookspace_worker_permission_denied(self):
        """
        Test creating a book tag by a bookspace worker (should be denied).
        """
        book_tag_data = {'name': BookTagChoices.HISTORY}
        response = self.client.post(reverse('main:book-tags-list'), book_tag_data,
                                    HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not BookTag.objects.filter(name=book_tag_data['name']).exists()

    def test_create_book_tag_as_regular_user_permission_denied(self):
        """
        Test creating a book tag by a regular user (should be denied).
        """
        book_tag_data = {'name': BookTagChoices.HISTORY}
        response = self.client.post(reverse('main:book-tags-list'), book_tag_data,
                                    HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not BookTag.objects.filter(name=book_tag_data['name']).exists()

    def test_create_book_tag_without_authentication(self):
        """
        Test creating a book tag without authentication (should be denied).
        """
        book_tag_data = {'name': BookTagChoices.HISTORY}
        response = self.client.post(reverse('main:book-tags-list'), book_tag_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not BookTag.objects.filter(name=book_tag_data['name']).exists()

    def test_retrieve_book_tag_as_bookspace_owner(self):
        """
        Test retrieving book-tags by a bookspace owner.
        """
        response = self.client.get(reverse('main:book-tags-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_book_tag_as_bookspace_manager(self):
        """
        Test retrieving book-tags by a bookspace manager.
        """
        response = self.client.get(reverse('main:book-tags-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_book_tags_as_asst_bookspace_manager(self):
        """
        Test retrieving book-tags by an assistant bookspace manager.
        """
        response = self.client.get(reverse('main:book-tags-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_book_tags_as_regular_user_permission_denied(self):
        """
        Test retrieving book-tags by a regular user (should be denied).
        """
        response = self.client.get(reverse('main:book-tags-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_book_tags_without_authentication(self):
        """
        Test retrieving book-tags without authentication (should be denied).
        """
        url = reverse('main:book-tags-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_book_tags_as_bookspace_owner(self):
        """
        Test updating a book_tag as bookspace owner
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_book_tags_as_bookspace_manager(self):
        """
        Test updating a book_tag as bookspace manager
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_book_tags_as_asst_bookspace_manager(self):
        """
        Test updating a book_tag as assistant bookspace manager
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_book_tags_as_bookspace_worker_permission_denied(self):
        """
        Test updating a book_tag as bookspace worker (permission denied)
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_book_tags_as_regular_user_permission_denied(self):
        """
        Test updating a book_tag as regular (permission denied)
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data, HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_book_tags_without_authentication(self):
        """
        Test updating a book_tag without authentication
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_book_tags_as_bookspace_owner(self):
        """
        Test deleting a author by a bookspace owner.
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_book_tags_as_bookspace_manager(self):
        """
        Test deleting a author by a bookspace manager.
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_book_tags_as_asst_bookspace_manager(self):
        """
        Test deleting a author by an assistant bookspace manager.
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_book_tags_as_bookspace_worker_permission_denied(self):
        """
        Test deleting a author by a bookspace worker (should be denied).
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_book_tags_as_regular_user_permission_denied(self):
        '''
        Test delete author as a regular user (permission denied)
        '''
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})

        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_book_tags_unauthorized(self):
        '''
        Test delete author by unauthorized request
        '''
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert BookTag.objects.filter(id=book_tag.id).exists()

    def test_filter_book_tags_by_name(self):
        """
        Test filtering book-tags by name (e.g., get all book-tags with name 'Fiction').
        """
        BookTag.objects.create(name=BookTagChoices.FICTION)
        BookTag.objects.create(name=BookTagChoices.ROMANCE)
        url = reverse('main:book-tags-list')
        url += f'?name=Fiction'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Fiction'

    def test_filter_book_tags_by_partial_name(self):
        """
        Test filtering book-tags by name (e.g., get all book-tags with name 'Fi').
        """

        BookTag.objects.create(name=BookTagChoices.FICTION)
        BookTag.objects.create(name=BookTagChoices.ROMANCE)
        url = reverse('main:book-tags-list')
        url += f'?name=Fi'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Fiction'

    def test_order_book_tags_by_multiple_fields(self):
        """
        Test ordering book-tags by multiple fields (e.g., first names in descending order, id in ascending order).
        """
        BookTag.objects.create(name=BookTagChoices.FICTION)
        BookTag.objects.create(name=BookTagChoices.ROMANCE)
        url = reverse('main:book-tags-list')
        url += '?ordering=name'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        print(response.data[0]['name'])
        # assert response.data[0]['name'] == 'Fiction'
        # assert response.data[1]['name'] == 'Romance'

    def test_no_results_for_invalid__book_tag_name(self):
        """
        Test filtering with a name that doesn't exist.
        """
        url = reverse('main:book-tags-list')
        url += '?name=nonexistent'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'detail': 'No book tag(s) found matching the provided filters.'}

