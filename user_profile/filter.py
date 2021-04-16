import django_filters
from django.db.models import Q
from django.forms import Select
from orders.models import Order


class OrderFilter(django_filters.FilterSet):
    CHOICES = (
        ('any', 'Any'),
        ('progress', 'In progress'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )

    status = django_filters.ChoiceFilter(choices=CHOICES,
                                         method='filter_by_status',
                                         empty_label=None,
                                         widget=Select(
                                             attrs={'class': 'selectpicker show-tick form-control',
                                                    'data-placeholder': '$ USD'
                                                    })
                                         )

    class Meta:
        model = Order
        fields = ['status']

    def filter_by_status(self, queryset, name, value):
        if value == 'progress':
            queryset = queryset.filter(~Q(status__in=['Delivered', 'Received', 'Canceled']))

        if value == 'delivered':
            queryset = queryset.filter(status='Delivered')

        if value == 'completed':
            queryset = queryset.filter(status='Received')

        if value == 'canceled':
            queryset = queryset.filter(status='Canceled')

        return queryset
