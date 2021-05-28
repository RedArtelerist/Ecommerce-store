import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views import View
from django.views.decorators.http import require_POST
from cart.forms import CartAddProductForm
from store.filter import ProductFilter, SearchProductFilter
from store.forms import CommentForm, ReviewForm
from store.models import *
from store.utils import get_products_by_filter_and_pagination, get_price


def index(request):
    companies = sorted(Company.objects.all(), key=lambda t: t.popular, reverse=True)

    discount_products = Product.objects.filter(discount__gte=5, available=True).order_by('-discount')[:16]
    best_seller = Product.objects.filter(available=True).order_by('-sales')[:16]

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


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    cart_product_form = CartAddProductForm()
    comments = product.comments()

    return render(request, 'store/product_detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'comments': comments})


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


@require_POST
def add_comment(request, pk):
    form = CommentForm(request.POST)
    product = Product.objects.get(id=pk)
    if form.is_valid():
        form = form.save(commit=False)

        if request.user.is_authenticated:
            form.user = request.user

        if request.POST.get("parent", None) and id == 0:
            print(request.POST.get("parent"))
            form.parent_id = int(request.POST.get("parent"))

        form.product = product
        form.save()

    return redirect(product.get_absolute_url())


@require_POST
@login_required(login_url='/accounts/login/')
def delete_comment(request, id):
    comment = Comment.objects.get(pk=id)
    product = comment.product
    comment.delete()
    return redirect(product.get_absolute_url())


@login_required(login_url='/accounts/login/')
@require_POST
def add_review(request, pk):
    form = ReviewForm(request.POST)
    product = Product.objects.get(id=pk)
    if form.is_valid():
        form = form.save(commit=False)

        if request.user.is_authenticated:
            form.user = request.user

        form.product = product
        form.save()

    return redirect(product.get_absolute_url())


@require_POST
def delete_review(request, id):
    review = Review.objects.get(pk=id)
    product = review.product
    review.delete()
    return redirect(product.get_absolute_url())


class VotesView(View):
    model = None
    vote_type = None

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        try:
            like_dislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj),
                                                   object_id=obj.id,
                                                   user=request.user)
            if like_dislike.vote is not self.vote_type:
                like_dislike.vote = self.vote_type
                like_dislike.save(update_fields=['vote'])
                result = True
            else:
                like_dislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )