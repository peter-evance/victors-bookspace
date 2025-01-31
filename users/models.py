from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField

from users.choices import *
from users.validators import *


class CustomUser(AbstractUser):
    """
    Custom user model representing a user in the bookspace management system.

    Fields:
    - `username`: A unique character field representing the username of the user.
                  It is limited to a maximum length of 45 characters.
    - `first_name`: A character field representing the first name of the user.
                     It is limited to a maximum length of 20 characters.
    - `last_name`: A character field representing the last name of the user.
                    It is limited to a maximum length of 20 characters.
    - `phone_number`: A phone number field representing the phone number of the user.
                      It is limited to a maximum length of 13 characters and must be unique.
    - `sex`: A character field representing the gender of the user.
             The available choices are defined in the `SexChoices` enum.
             It is limited to a maximum length of 6 characters.
    - `is_bookspace_owner`: A boolean field representing whether the user is a bookspace owner.
    - `is_bookspace_manager`: A boolean field representing whether the user is a bookspace manager.
    - `is_assistant_bookspace_manager`: A boolean field representing whether the user is an assistant bookspace manager.
    - `is_bookspace_worker`: A boolean field representing whether the user is a bookspace worker.

    Methods:
    - `assign_bookspace_owner()`: Assigns the user as a bookspace owner and updates related fields accordingly.
    - `assign_bookspace_manager()`: Assigns the user as a bookspace manager and updates related fields accordingly.
    - `assign_assistant_bookspace_manager()`: Assigns the user as an assistant bookspace manager and updates related fields accordingly.
    - `assign_bookspace_worker()`: Assigns the user as a bookspace worker and updates related fields accordingly.
    - `dismiss_bookspace_owner()`: Dismisses the user from the bookspace owner role.
    - `dismiss_bookspace_manager()`: Dismisses the user from the bookspace manager role.
    - `dismiss_assistant_bookspace_manager()`: Dismisses the user from the assistant bookspace manager role.
    - `dismiss_bookspace_worker()`: Dismisses the user from the bookspace worker role.
    - `get_full_name()`: Returns the full name of the user.
    - `get_role()`: Returns the role of the user based on their assigned roles.
    - `get_bookspace_workers()`: Retrieves all bookspace workers associated with the user.
    - `get_bookspace_managers()`: Retrieves all bookspace managers associated with the user.
    - `get_bookspace_owners()`: Retrieves all bookspace owners associated with the user.
    - `generate_username(first_name, last_name)`: Generates a unique username based on the user's first name and last name.
    """

    username = models.CharField(max_length=45, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = PhoneNumberField(max_length=13, unique=True)
    sex = models.CharField(choices=SexChoices.choices, max_length=6)
    is_bookspace_owner = models.BooleanField(default=False)
    is_bookspace_manager = models.BooleanField(default=False)
    is_assistant_bookspace_manager = models.BooleanField(default=False)
    is_bookspace_worker = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'sex']

    def assign_bookspace_owner(self):
        self.is_bookspace_owner = True
        self.is_bookspace_manager = False
        self.is_assistant_bookspace_manager = False
        self.is_bookspace_worker = False
        self.save()

    def assign_bookspace_manager(self):
        self.is_bookspace_owner = False
        self.is_bookspace_manager = True
        self.is_assistant_bookspace_manager = False
        self.is_bookspace_worker = False
        self.save()

    def assign_assistant_bookspace_manager(self):
        self.is_bookspace_owner = False
        self.is_bookspace_manager = False
        self.is_assistant_bookspace_manager = True
        self.is_bookspace_worker = False
        self.save()

    def assign_bookspace_worker(self):
        self.is_bookspace_owner = False
        self.is_bookspace_manager = False
        self.is_assistant_bookspace_manager = False
        self.is_bookspace_worker = True
        self.save()

    def dismiss_bookspace_owner(self):
        self.is_bookspace_owner = False
        self.save()

    def dismiss_bookspace_manager(self):
        self.is_bookspace_manager = False
        self.save()

    def dismiss_assistant_bookspace_manager(self):
        self.is_assistant_bookspace_manager = False
        self.save()

    def dismiss_bookspace_worker(self):
        self.is_bookspace_worker = False
        self.save()

    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    def get_role(self):
        """Return the role of the user."""
        if self.is_bookspace_owner:
            return "Bookspace Owner"
        elif self.is_bookspace_manager:
            return "Bookspace Manager"
        elif self.is_assistant_bookspace_manager:
            return "Assistant Bookspace Manager"
        elif self.is_bookspace_worker:
            return "Bookspace Worker"
        else:
            return "Regular User"

    def get_bookspace_workers(self):
        return CustomUser.objects.filter(is_bookspace_worker=True)

    def get_bookspace_managers(self):
        return CustomUser.objects.filter(is_bookspace_manager=True)

    def get_bookspace_owners(self):
        return CustomUser.objects.filter(is_bookspace_owner=True)

    def clean(self):
        CustomUserValidator.validate_sex(self.sex)
        CustomUserValidator.validate_username(self.username)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_username(first_name, last_name):
        base_username = slugify(f"{first_name}-{last_name}")
        username = base_username
        counter = 1

        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}-{counter}"
            counter += 1

        return username
