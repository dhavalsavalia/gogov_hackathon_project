import django_filters
from .models import Scholarship

class ScholarshipFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Scholarship
        fields = ['type_of_scholorship', 'stream', 'income', 'caste']
