from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.wishlist_detail, name='wishlist_detail'),
    re_path(r'^add/(?P<product_id>\d+)/$', views.wishlist_add, name='wishlist_add'),
    re_path(r'^remove/(?P<product_id>\d+)/$', views.wishlist_remove, name='wishlist_remove'),
]