from django.urls import re_path

from user_profile import views

urlpatterns = [
    re_path(r'^personal_info', views.personal_info, name='personal_info'),
    re_path(r'^change_password', views.change_password, name='change_password'),
    re_path(r'^account_settings', views.account_settings, name='account_settings'),
    re_path(r'^orders', views.orders, name='orders'),
    re_path(r'^order/(?P<order_id>[-\w]+)/$', views.order_detail, name='order_detail'),
    re_path(r'^connections', views.connections, name='connections'),
    re_path(r'^cancel_order/(?P<order_id>[-\w]+)/$', views.cancel_order, name='cancel_order'),
    re_path(r'^delete_account', views.delete_account, name='delete_account'),

]