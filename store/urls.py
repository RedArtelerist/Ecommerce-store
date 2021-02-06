from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from store import views
from cart import views as cart_views

urlpatterns = [
    path('', views.index, name='home'),
    url(r'^$', views.product_list, name='product_list'),
    path('search/', views.search, name='search_products'),
    url(r'^ajax_calls/search/', views.autocompleteModel),
    path('cart_update/', cart_views.cart_update, name='cart_update'),

    url(r'^category/(?P<category_slug>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),

    url(r'^brend/(?P<company_slug>[-\w]+)/$',
        views.product_list_by_company,
        name='product_list_by_company'),

    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.product_detail,
        name='product_detail'),

]
