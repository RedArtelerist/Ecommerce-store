import json
from django.db.models import *
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from store.filter import ProductFilter, SearchProductFilter
from store.models import *
from store.utils import get_products_by_filter_and_pagination


def index(request):
    companies = sorted(Company.objects.all(), key=lambda t: t.popular, reverse=True)

    discount_products = Product.objects.filter(discount__gte=5, available=True).order_by('-discount')[:16]
    best_seller = Product.objects.filter(available=True).order_by('-sales')[:16]
    #newest_products =

    return render(request, 'store/home.html',
                  {'title': 'Home page',
                   'companies': companies,
                   'discounts': discount_products,
                   'best_seller': best_seller})


def product_list(request, category_slug=None):
    category = None
    products_list = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        if category.get_descendants():
            products = Product.objects.filter(category__in=category.get_descendants())
            return render(request, 'store/category_list.html',
                          {'category': category,
                           'products': products.order_by('-sales')[:10]})

        products_list = products_list.filter(category=category).order_by('-available', '-sales')

    f = ProductFilter(request.GET, request=category, queryset=products_list)

    price = get_price(request, products_list)

    count, products = get_products_by_filter_and_pagination(request, f)

    context = {'category': category,
               'filter': f,
               'products': products,
               'count': count,
               'min_price': price['min_price'],
               'max_price': price['max_price']}

    return render(request, 'store/product_list.html', context)


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


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    cart_product_form = CartAddProductForm()
    return render(request, 'store/product_detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


def product_list_by_company(request, company_slug=None):
    if company_slug:
        company = get_object_or_404(Company, slug=company_slug)
        categories_by_company = Category.objects.filter(
            slug__in=Product.objects.filter(company=company).values_list(
                'category__slug', flat=True).distinct().order_by()
        )
        return render(request,
                      'store/company_products.html',
                      {'company': company,
                       'company_categories': categories_by_company})


def search(request):
    str_query = str(request.GET.get('query'))

    if len(str_query.strip()) <= 3:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    products = Product.objects.filter(
        Q(name__icontains=str_query) |
        Q(company__name__icontains=str_query)
    ).order_by('-available', '-sales').distinct()

    categories_ids = products.values_list("category_id", flat=True).distinct()
    categories = Category.objects.filter(pk__in=categories_ids)

    f = SearchProductFilter(request.GET, request=categories, queryset=products)

    count, products = get_products_by_filter_and_pagination(request, f)

    return render(request, 'store/search.html', {
        'filter': f,
        'query': str(request.GET.get('query')),
        'count': count,
        'products': products})


def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Product.objects.filter(
            Q(name__icontains=q) |
            Q(company__name__icontains=q)).order_by('-sales')

        results = [x.name for x in search_qs]
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)