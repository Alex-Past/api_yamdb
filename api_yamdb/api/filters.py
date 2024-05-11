from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = filters.CharFilter(
        field_name='category__slug', lookup_expr='icontains'
    )
    genre = filters.CharFilter(
        field_name='genre__slug', lookup_expr='icontains'
    )
    year = filters.CharFilter(field_name='year')

    class Meta:
        model = Title
        fields = '__all__'
