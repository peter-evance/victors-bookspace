from django_filters import rest_framework as filters
from main.models import *


class AuthorFilterSet(filters.FilterSet):
    first_name = filters.CharFilter(lookup_expr="icontains")
    last_name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Author
        fields = ["first_name", "last_name"]


class BookTagFilterSet(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = BookTag
        fields = ["name"]
