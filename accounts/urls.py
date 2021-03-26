from django.conf.urls import url
from django.urls import path
from accounts import views, utils

urlpatterns = [
    url(r'^register/', views.register_request, name='register'),
    path('activate/<uidb64>/<token>/', utils.activate, name='activate'),
    url(r'^login/', views.login_request, name='login'),
    url(r'^logout/', views.logout_request, name='logout'),
    path('password_reset/', utils.password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>', utils.password_reset_confirm, name='password_reset_confirm'),
]