import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from users.choices import *
from main.models import *

User = get_user_model()


@pytest.fixture()
@pytest.mark.django_db
def setup_users():
    client = APIClient()

    # Create bookspace owner user
    bookspace_owner_data = {
        'username': 'owner@example.com',
        'password': 'testpassword',
        'first_name': 'Book_Space',
        'last_name': 'Owner',
        'phone_number': '+254787654321',
        'sex': SexChoices.MALE,
        'is_bookspace_owner': True,
    }
    bookspace_owner_login_data = {
        'username': 'owner@example.com',
        'password': 'testpassword',
    }
    response = client.post('/auth/users/', bookspace_owner_data)
    bookspace_owner_user_id = response.data['id']
    bookspace_owner_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), bookspace_owner_login_data)
    bookspace_owner_token = response.data['auth_token']

    # Create bookspace manager user
    bookspace_manager_data = {
        'username': 'manager@example.com',
        'password': 'testpassword',
        'first_name': 'Bookspace',
        'last_name': 'Manager',
        'phone_number': '+254755555555',
        'sex': SexChoices.MALE,
        'is_bookspace_manager': True,
    }
    bookspace_manager_login_data = {
        'username': 'manager@example.com',
        'password': 'testpassword'
    }
    response = client.post('/auth/users/', bookspace_manager_data)
    bookspace_manager_user_id = response.data['id']
    bookspace_manager_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), bookspace_manager_login_data)
    bookspace_manager_token = response.data['auth_token']

    # Create assistant bookspace manager user
    asst_bookspace_manager_data = {
        'username': 'assistant@example.com',
        'password': 'testpassword',
        'first_name': 'Assistant',
        'last_name': 'Bookspace Manager',
        'phone_number': '+254744444444',
        'sex': SexChoices.FEMALE,
        'is_assistant_bookspace_manager': True,
    }
    asst_bookspace_manager_login_data = {
        'username': 'assistant@example.com',
        'password': 'testpassword',
    }
    response = client.post('/auth/users/', asst_bookspace_manager_data)
    asst_bookspace_manager_user_id = response.data['id']
    asst_bookspace_manager_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), asst_bookspace_manager_login_data)
    asst_bookspace_manager_token = response.data['auth_token']

    # Create bookspace worker user
    bookspace_worker_data = {
        'username': 'worker@example.com',
        'password': 'testpassword',
        'first_name': 'Bookspace',
        'last_name': 'Worker',
        'phone_number': '+254722222222',
        'sex': SexChoices.FEMALE,
        'is_bookspace_worker': True,
    }
    bookspace_worker_login_data = {
        'username': 'worker@example.com',
        'password': 'testpassword',
    }
    response = client.post('/auth/users/', bookspace_worker_data)
    bookspace_worker_user_id = response.data['id']
    bookspace_worker_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), bookspace_worker_login_data)
    bookspace_worker_token = response.data['auth_token']

    # Create regular user
    regular_user_data = {
        'username': 'test@example.com',
        'password': 'testpassword',
        'first_name': 'John',
        'last_name': 'Doe',
        'phone_number': '+254712345678',
        'sex': SexChoices.MALE,
    }
    regular_user_login_data = {
        'username': 'test@example.com',
        'password': 'testpassword',
    }

    response = client.post('/auth/users/', regular_user_data)
    regular_user_id = response.data['id']
    regular_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), regular_user_login_data)
    regular_user_token = response.data['auth_token']

    return {
        'client': client,

        'regular_user_id': regular_user_id,
        'regular_user_token': regular_user_token,
        'regular_user_username': regular_user_username,

        'bookspace_owner_token': bookspace_owner_token,
        'bookspace_owner_user_id': bookspace_owner_user_id,
        'bookspace_owner_user_username': bookspace_owner_user_username,

        'bookspace_manager_token': bookspace_manager_token,
        'bookspace_manager_user_id': bookspace_manager_user_id,
        'bookspace_manager_user_username': bookspace_manager_user_username,

        'asst_bookspace_manager_token': asst_bookspace_manager_token,
        'asst_bookspace_manager_user_id': asst_bookspace_manager_user_id,
        'asst_bookspace_manager_user_username': asst_bookspace_manager_user_username,

        'bookspace_worker_token': bookspace_worker_token,
        'bookspace_worker_user_id': bookspace_worker_user_id,
        'bookspace_worker_user_username': bookspace_worker_user_username,
    }


@pytest.fixture()
@pytest.mark.django_db
def setup_book_data():
    author = Author.objects.create(first_name='Niccolò', last_name='Machiavelli')
    book_tag = BookTag.objects.create(name=BookTagChoices.HISTORY)
    book_data = {
        "name": "The Prince",
        "author": author.id,
        "tags": book_tag.id,
        "price": 99.99,
    }
    return {'book_data': book_data}
