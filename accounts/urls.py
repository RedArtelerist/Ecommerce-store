from django.urls import path, include, re_path
from accounts import views, utils

urlpatterns = [
    re_path(r'^register/', views.register_request, name='register'),
    path('activate/<uidb64>/<token>/', utils.activate, name='activate'),
    re_path(r'^login/', views.login_request, name='login'),
    re_path(r'^logout/', views.logout_request, name='logout'),
    path('password_reset/', utils.password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>', utils.password_reset_confirm, name='password_reset_confirm')
]