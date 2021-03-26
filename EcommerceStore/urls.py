from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('store.urls')),
    url(r'^accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    url(r'^wishlist/', include(('wishlist.urls', 'wishlist'), namespace='wishlist')),
    url(r'^cart/', include(('cart.urls', 'cart'), namespace='cart')),
    url(r'^order/', include(('orders.urls', 'orders'), namespace='orders')),
    url(r'^coupons/', include(('coupons.urls', 'coupons'), namespace='coupons')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
