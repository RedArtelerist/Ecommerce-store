from django.urls import re_path, path

from orders import views

urlpatterns = [
    re_path(r'^(?P<order_id>\d+)/$', views.order_success, name='order_success'),
    path('', views.order_create, name='checkout'),
]