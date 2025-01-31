from phonenumber_field.modelfields import PhoneNumberField

from main.choices import *


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


class BookTag(models.Model):
    name = models.CharField(choices=BookTagChoices.choices, max_length=16)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name='books')
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(BookTag, blank=True)
    publication_date = models.DateField(null=True)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_display_image(self):
        """Returns the best available image for display."""
        book_image = self.bookimages.first()
        if book_image:
            return book_image.thumbnail or book_image.cover_image
        return None

    def get_image_url(self):
        """Returns the URL of the best available image."""
        image = self.get_display_image()
        return image.url if image else None


class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookimages')
    cover_image = models.ImageField(upload_to='book-covers')
    thumbnail = models.ImageField(upload_to='book-thumbnails', null=True, editable=False)


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.price_at_time:
            self.price_at_time = self.book.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.book.title}"


class BookInventory(models.Model):
    name = models.OneToOneField(Book, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()

    def add_to_stock_quantity(self):
        self.stock_quantity + 1
        self.save()

    def deduct_stock_quantity(self):
        if self.stock_quantity > 0:
            self.stock_quantity - 1
            self.save()

