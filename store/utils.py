from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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