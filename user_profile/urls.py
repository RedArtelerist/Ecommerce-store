from django.conf.urls import url
from user_profile import views

urlpatterns = [
    url(r'^personal_info', views.personal_info, name='personal_info'),
    url(r'^change_password', views.change_password, name='change_password'),
    url(r'^account_settings', views.account_settings, name='account_settings'),
    url(r'^orders', views.orders, name='orders'),
    url(r'^order/(?P<order_id>[-\w]+)/$', views.order_detail, name='order_detail'),
    url(r'^connections', views.connections, name='connections'),
    url(r'^cancel_order/(?P<order_id>[-\w]+)/$', views.cancel_order, name='cancel_order'),
    url(r'^delete_account', views.delete_account, name='delete_account'),

]