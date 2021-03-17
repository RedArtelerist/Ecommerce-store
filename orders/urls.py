from django.conf.urls import url
from orders import views

urlpatterns = [
    url(r'^$', views.order_create, name='checkout'),
]