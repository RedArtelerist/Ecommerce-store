from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Min, Max, F, Value, IntegerField


def get_products_by_filter_and_pagination(request, f):
    count = f.qs.count()
    paginator = Paginator(f.qs, 9)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return count, products


def get_price(request, queryset):
    companies = request.GET.getlist('company')
    years = request.GET.getlist('year')
    name = request.GET.get('name')
    order = request.GET.get('order')

    if len(companies) != 0:
        queryset = queryset.filter(company__slug__in=companies)

    if len(years) != 0:
        queryset = queryset.filter(year__in=years)

    if name != "" and name is not None:
        queryset = queryset.filter(name__contains=name)

    if order == 'action':
        queryset = queryset.filter(discount__gte=5)

    price = queryset.aggregate(
        min_price=Min((Value(1.0) - F('discount') / Value(100.0)) * F('price'), output_field=IntegerField()),
        max_price=Max((Value(1.0) - F('discount') / Value(100.0)) * F('price'), output_field=IntegerField())
    )
    return price