from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('store.urls')),
    re_path(r'^accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    re_path(r'^wishlist/', include(('wishlist.urls', 'wishlist'), namespace='wishlist')),
    re_path(r'^cart/', include(('cart.urls', 'cart'), namespace='cart')),
    re_path(r'^order/', include(('orders.urls', 'orders'), namespace='orders')),
    re_path(r'^profile/', include(('user_profile.urls', 'profile'), namespace='profile')),
    re_path(r'^coupons/', include(('coupons.urls', 'coupons'), namespace='coupons')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('telegram/', include('telegram_bot.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)