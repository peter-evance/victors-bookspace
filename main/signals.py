from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import *
from PIL import Image
import os
from django.conf import settings


@receiver(post_save, sender=BookImage)
def generate_thumbnail(sender, instance, **kwargs):
    if instance.cover_image and not instance.thumbnail:
        try:
            img = Image.open(instance.cover_image.path)

            thumbnail_size = (100, 100)
            img.thumbnail(thumbnail_size)

            book_name = instance.book.name.replace(" ", "-")

            thumbnail_filename = f"{book_name}-thumbnail.png"

            thumbnail_path = os.path.join(settings.MEDIA_ROOT, "book-thumbnails", thumbnail_filename)
            img.save(thumbnail_path, "PNG")

            # Update the thumbnail field in the model with the relative path inside the MEDIA_URL
            instance.thumbnail.name = os.path.join("book-thumbnails", thumbnail_filename)
            instance.save()
        except Exception as error:

            print(f"Thumbnail generation failed: {error}")


@receiver(post_save, sender=Book)
def create_book_inventory(sender, instance, created, **kwargs):
    """
    Signal to automatically create a BookInventory instance when a new Book is created.
    Sets initial stock quantity to 0.
    """
    if created:  # Only run this when a new Book is created, not on updates
        BookInventory.objects.create(
            name=instance,
            stock_quantity=0  # Starting with 0 stock
        )
