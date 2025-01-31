from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from main.filters import *
from main.permissions import *
from main.serializers import *


def contact_view(request):
    return render(request, 'main/contact_us.html')


class MainView(ListView):
    model = Book
    template_name = 'main/main.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        queryset = Book.objects.all().prefetch_related('authors', 'tags', 'bookimages')

        # Search functionality
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(authors__first_name__icontains=query) |
                Q(authors__last_name__icontains=query) |
                Q(isbn__icontains=query)
            ).distinct()

        # Tag filtering
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__name=tag)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = BookTag.objects.all()
        context['current_tag'] = self.request.GET.get('tag')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AuthorFilterSet
    ordering_fields = ["first_name", "last_name"]
    permission_classes = [CanActOnAuthor]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching authors
                return Response(
                    {"detail": "No author(s) found matching the provided filters."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no authors in the database
                return Response(
                    {"detail": "No authors found in the shop yet."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BookTagViewSet(viewsets.ModelViewSet):
    queryset = BookTag.objects.all()
    serializer_class = BookTagSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BookTagFilterSet
    ordering_fields = ["name"]
    permission_classes = [CanActOnBookTag]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching book tags
                return Response(
                    {"detail": "No book tag(s) found matching the provided filters."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no book tags in the database
                return Response(
                    {"detail": "No book tags found in the shop yet."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BookImageViewSet(viewsets.ModelViewSet):
    queryset = BookImage.objects.all()
    serializer_class = BookImageSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [CanAddBookImage]
        elif self.action == "destroy":
            permission_classes = [CanDeleteBookImage]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [CanUpdateBookImage]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [CanAddBook]
        elif self.action == "destroy":
            permission_classes = [CanDeleteBook]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [CanUpdateBook]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
