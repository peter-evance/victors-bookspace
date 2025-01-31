from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    """
    Admin class for managing `CustomUser` instances in the Django admin panel.
    Provides comprehensive user management capabilities including role assignments.
    """
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'get_role',
        'is_active',
        'is_staff',
    )

    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'is_bookspace_owner',
        'is_bookspace_manager',
        'is_assistant_bookspace_manager',
        'is_bookspace_worker',
        'sex',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'phone_number',
    )

    ordering = ('username',)

    fieldsets = (
        (_("Personal Info"), {
            "fields": (
                "username",
                "password",
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "sex",
            ),
        }),
        (_("Roles & Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "is_bookspace_owner",
                "is_bookspace_manager",
                "is_assistant_bookspace_manager",
                "is_bookspace_worker",
                "groups",
                "user_permissions",
            ),
        }),
        (_("Important Dates"), {
            "fields": (
                "last_login",
                "date_joined",
            ),
            "classes": ("collapse",),
        }),
    )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': (
    #             'username',
    #             'first_name',
    #             'last_name',
    #             'email',
    #             'phone_number',
    #             'sex',
    #             'password1',
    #             'password2',
    #         ),
    #     }),
    # )

    readonly_fields = ('last_login', 'date_joined')

    actions = [
        'assign_bookspace_owner',
        'assign_bookspace_manager',
        'assign_assistant_bookspace_manager',
        'assign_bookspace_worker',
        'dismiss_all_roles'
    ]

    def get_role(self, obj):
        """Display the user's current role"""
        return obj.get_role()

    get_role.short_description = "Role"

    def assign_bookspace_owner(self, request, queryset):
        """Assign selected users as bookspace owners"""
        for user in queryset:
            user.assign_bookspace_owner()
        self.message_user(request, f"Successfully assigned {queryset.count()} users as Bookspace Owners")

    assign_bookspace_owner.short_description = "Assign as Bookspace Owner"

    def assign_bookspace_manager(self, request, queryset):
        """Assign selected users as bookspace managers"""
        for user in queryset:
            user.assign_bookspace_manager()
        self.message_user(request, f"Successfully assigned {queryset.count()} users as Bookspace Managers")

    assign_bookspace_manager.short_description = "Assign as Bookspace Manager"

    def assign_assistant_bookspace_manager(self, request, queryset):
        """Assign selected users as assistant bookspace managers"""
        for user in queryset:
            user.assign_assistant_bookspace_manager()
        self.message_user(request, f"Successfully assigned {queryset.count()} users as Assistant Bookspace Managers")

    assign_assistant_bookspace_manager.short_description = "Assign as Assistant Bookspace Manager"

    def assign_bookspace_worker(self, request, queryset):
        """Assign selected users as bookspace workers"""
        for user in queryset:
            user.assign_bookspace_worker()
        self.message_user(request, f"Successfully assigned {queryset.count()} users as Bookspace Workers")

    assign_bookspace_worker.short_description = "Assign as Bookspace Worker"

    def dismiss_all_roles(self, request, queryset):
        """Remove all bookspace roles from selected users"""
        for user in queryset:
            user.dismiss_bookspace_owner()
            user.dismiss_bookspace_manager()
            user.dismiss_assistant_bookspace_manager()
            user.dismiss_bookspace_worker()
        self.message_user(request, f"Successfully removed all roles from {queryset.count()} users")

    dismiss_all_roles.short_description = "Remove all bookspace roles"
