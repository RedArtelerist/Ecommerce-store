from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^wishlist/', include(('wishlist.urls', 'wishlist'), namespace='wishlist')),
    url(r'^cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('', include('store.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
