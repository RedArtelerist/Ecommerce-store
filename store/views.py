from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import *
from django.db.models.functions import Round
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from store.filter import ProductFilter
from store.models import *


def index(request):
    categories = Category.objects.all()
    companies = sorted(Company.objects.all(), key=lambda t: t.popular, reverse=True)

    discount_products = Product.objects.filter(discount__gte=5).order_by('-discount')[:16]
    best_seller = Product.objects.order_by('-sales')[:16]
    #newest_products =

    return render(request, 'store/home.html',
                  {'title': 'Home page',
                   'categories': categories,
                   'companies': companies,
                   'discounts': discount_products,
                   'best_seller': best_seller})


def product_list(request, category_slug=None):
    category = None

    categories = Category.objects.all()
    products_list = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        if category.get_descendants():
            #Create some template
            return HttpResponse("Not Found")
        products_list = products_list.filter(category=category).order_by('-sales')

    f = ProductFilter(request.GET, request=category, queryset=products_list)

    price = get_price(request, products_list)

    count = f.qs.count()
    paginator = Paginator(f.qs, 9)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'category': category,
               'categories': categories,
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
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request,
                  'store/product_detail.html',
                  {'categories': categories,
                   'product': product})


def product_list_by_company(request, company_slug=None):
    if company_slug:
        company = get_object_or_404(Company, slug=company_slug)
        categories = Category.objects.filter(
            slug__in=Product.objects.filter(company=company).values_list(
                'category__slug', flat=True).distinct().order_by()
        )
        return render(request,
                      'store/company_products.html',
                      {'company': company,
                       'categories': categories})