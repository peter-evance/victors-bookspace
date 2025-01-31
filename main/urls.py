from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import *


app_name = "main"

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'books', BookViewSet, basename='books')
router.register(r'books-tags', BookTagViewSet, basename='book-tags')
router.register(r'books-images', BookImageViewSet, basename='book-images')


urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('contact/', contact_view, name='contact_us'),
    path('api/', include(router.urls)),
]
