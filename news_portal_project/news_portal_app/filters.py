from django_filters import FilterSet, CharFilter, DateFilter
from django.forms.widgets import DateInput
from .models import Post


class NewsFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains', label='Title')
    date = DateFilter(
        widget=DateInput(attrs={'pattern': 'YYYY-MM-DD', 'type': 'date'}),
        lookup_expr='gte',
        label='Not older than'
    )
    author__user__username = CharFilter(lookup_expr='icontains', label='Author')

    class Meta:
        model = Post
        fields = ['name', 'date']
