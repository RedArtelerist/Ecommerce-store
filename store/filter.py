import django_filters
from django.db.models import Case, When, Value, F, ExpressionWrapper, Q
from django.forms import *

from store.models import *


def get_companies(request):
    if request is None:
        return Company.objects.none()

    category = request
    companies = Product.objects.filter(category=category).values_list('company__slug', flat=True).distinct()

    return Company.objects.filter(slug__in=companies).order_by('name')


def get_categories(request):
    if request is None:
        return Category.objects.none()

    categories = request
    return categories


def get_years():
    return tuple(Product.objects.all().values_list('year', 'year').distinct().order_by('-year'))


class ProductFilter(django_filters.FilterSet):
    CHOICES = (
        ('popular', 'Popularity'),
        ('price-asc', 'Low Price → High Price'),
        ('price-desc', 'High Price → Low Price'),
        ('rank', 'Rating'),
        ('action', 'Promotional'),
    )

    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Search here...'})
    )
    price = django_filters.RangeFilter(method='filter_by_price')
    order = django_filters.ChoiceFilter(choices=CHOICES,
                                        method='filter_by_order',
                                        empty_label=None,
                                        widget=Select(
                                            attrs={'class': 'selectpicker show-tick form-control',
                                                   'data-placeholder': '$ USD'
                                                   })
                                        )

    company = django_filters.ModelMultipleChoiceFilter(
        queryset=get_companies,
        field_name="company__slug",
        to_field_name="slug",
        widget=CheckboxSelectMultiple(),
        label="Company",
        label_suffix="",
    )

    year = django_filters.MultipleChoiceFilter(
        choices=get_years,
        field_name="year",
        widget=CheckboxSelectMultiple(),
        label="Year",
        label_suffix="",
    )

    class Meta:
        model = Product
        fields = ['name', 'company', 'year', 'order']

    def filter_by_price(self, queryset, name, value):
        queryset.annotate(
            discount_price=ExpressionWrapper((Value(1.0) - F('discount') / Value(100.0)) * F('price'),
                                             output_field=IntegerField())
        )
        filtered = [x for x in queryset if value.start <= x.discount_price <= value.stop]
        pk_list = [x.id for x in filtered]

        return queryset.filter(pk__in=pk_list)

    def filter_by_order(self, queryset, name, value):
        if value == 'action':
            queryset = queryset.filter(discount__gte=5)

        if value == 'popular' or value == 'action':
            tuples = [(r.id, r.sales) for r in queryset]
        else:
            tuples = [(r.id, r.discount_price) for r in queryset]
        sort_list = sorted(tuples, key=lambda x: x[1])
        pk_list = [idx for idx, rating in sort_list]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
        if value == 'price-desc' or value == 'popular' or value == 'action':
            preserved = -preserved

        queryset = queryset.filter(pk__in=pk_list).order_by(preserved)
        return queryset


class SearchProductFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(
        field_name="name",
        method="filter_by_name",
        lookup_expr="icontains",
        widget=HiddenInput()
    )
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=get_categories,
        field_name="category__slug",
        to_field_name="slug",
        widget=CheckboxSelectMultiple(),
        label="Category",
        label_suffix="",
    )

    def filter_by_name(self, queryset, name, value):
        return queryset