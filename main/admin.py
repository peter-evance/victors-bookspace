from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline

from .models import *


@admin.register(Author)
class AuthorAdmin(ModelAdmin):
    """
    Admin class for managing `Author` instances in the Django admin panel.
    Provides a clean interface for viewing and editing author information.
    """
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    ordering = ('last_name', 'first_name')

    fieldsets = (
        (_("Author Information"), {
            "fields": ("first_name", "last_name", "bio"),
            "description": "Define and manage author details.",
        }),
    )


@admin.register(BookTag)
class BookTagAdmin(ModelAdmin):
    """
    Admin class for managing `BookTag` instances in the Django admin panel.
    """
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

    fieldsets = (
        (_("Tag Information"), {
            "fields": ("name", "description"),
            "description": "Define and manage book tags.",
        }),
    )


@admin.register(Book)
class BookAdmin(ModelAdmin):
    """
    Admin class for managing `Book` instances in the Django admin panel.
    Provides a user-friendly interface for viewing, filtering, and editing
    book information.
    """
    list_display = (
        'title',
        'isbn',
        'price',
        'publication_date',
        'date_updated',
        'get_authors',
    )

    search_fields = ('title', 'isbn', 'authors__first_name', 'authors__last_name')
    list_filter = ('tags', 'publication_date')
    ordering = ('title', 'publication_date')

    fieldsets = (
        (_("Basic Information"), {
            "fields": (
                "title",
                "authors",
                "description",
                "price",
            ),
        }),
        (_("Publication Details"), {
            "fields": (
                "publication_date",
                "isbn",
                "tags",
            ),
            "classes": ("collapse",),
        }),
    )

    def get_authors(self, obj):
        """Returns a comma-separated list of authors"""
        return ", ".join(str(author) for author in obj.authors.all())

    get_authors.short_description = "Authors"


@admin.register(BookImage)
class BookImageAdmin(ModelAdmin):
    """
    Admin class for managing `BookImage` instances in the Django admin panel.
    """
    list_display = ('book', 'cover_image', 'thumbnail')
    search_fields = ('book__title',)
    ordering = ('book',)


class OrderItemInline(TabularInline):
    """
    Inline admin for OrderItems, allowing them to be managed directly
    within the Order admin interface.
    """
    model = OrderItem
    extra = 1
    fields = ('book', 'quantity', 'price_at_time')
    readonly_fields = ('price_at_time',)


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    """
    Admin class for managing `Order` instances in the Django admin panel.
    Provides comprehensive order management capabilities.
    """
    list_display = (
        'id',
        'customer_name',
        'phone_number',
        'email',
        'status',
        'order_date',
        'total_amount',
    )

    search_fields = ('customer_name', 'email', 'phone_number')
    list_filter = ('status', 'order_date')
    ordering = ('-order_date',)

    inlines = [OrderItemInline]

    fieldsets = (
        (_("Customer Information"), {
            "fields": (
                "customer_name",
                "phone_number",
                "email",
            ),
        }),
        (_("Order Details"), {
            "fields": (
                "status",
                "total_amount",
                "notes",
            ),
            "classes": ("collapse",),
        }),
        (_("Timestamps"), {
            "fields": (
                "order_date",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ('order_date', 'updated_at')


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    """
    Admin class for managing `OrderItem` instances in the Django admin panel.
    """
    list_display = ('order', 'book', 'quantity', 'price_at_time')
    search_fields = ('order__customer_name', 'book__title')
    list_filter = ('order__status',)
    ordering = ('-order__order_date',)

    fieldsets = (
        (_("Order Information"), {
            "fields": (
                "order",
                "book",
                "quantity",
                "price_at_time",
            ),
        }),
    )


@admin.register(BookInventory)
class BookInventoryAdmin(ModelAdmin):
    """
    Admin class for managing `BookInventory` instances in the Django admin panel.
    """
    list_display = ('name', 'stock_quantity')
    search_fields = ('name__title',)
    ordering = ('name',)

    fieldsets = (
        (_("Inventory Information"), {
            "fields": (
                "name",
                "stock_quantity",
            ),
        }),
    )
