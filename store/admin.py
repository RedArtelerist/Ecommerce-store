from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin
from store.models import *


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'country']
    prepopulated_fields = {'slug': ('name',)}


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(label="Description", widget=CKEditorUploadingWidget())
    specifications = forms.CharField(label="Specifications", widget=CKEditorUploadingWidget())

    class Meta:
        description = Product
        fields = '__all__'


class ImagesInline(admin.TabularInline):
    model = ImageItem
    extra = 1
    classes = ('collapse',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        if obj.image.url:
            pass
        else:
            return mark_safe(f'<img src= width="100" style="max-height: 250px"')
        return mark_safe(f'<img src={obj.image.url} width="100" style="max-height: 250px"')

    get_image.short_description = 'Image'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'company', 'price', 'sales', 'available', 'created', 'updated', 'get_image']
    list_filter = ['category', 'company', 'year', 'available', 'created', 'updated']
    readonly_fields = ('get_image', 'sales')
    search_fields = ('name', 'category__name', 'company__name')
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True

    inlines = [ImagesInline]
    form = ProductAdminForm

    fieldsets = (
        (None, {
            "fields": (('image', 'get_image',),)
        }),
        (None, {
            "fields": (('name', 'slug',), 'description', 'shortSpecifications', 'specifications',)
        }),
        (None, {
            "fields": (('category', 'company'),)
        }),
        (None, {
            "fields": (('price', 'discount', 'year'),)
        }),
        (None, {
            "fields": ('sales', 'available')
        }),
    )

    def get_image(self, obj):
        if obj.image.url:
            pass
        else:
            return mark_safe(f'<img src= width="100" style="max-height: 250px"')
        return mark_safe(f'<img src={obj.image.url} width="100" style="max-height: 250px"')

    get_image.short_description = 'Image'

    def save_model(self, request, obj, form, change):
        product_id = str(obj.id)
        sessions = Session.objects.filter(expire_date__gte=timezone.now())

        for session in sessions:
            session_data = session.get_decoded()
            cart = session_data.get('cart')

            if cart and product_id in cart:
                if not obj.available:
                    cart.pop(product_id, None)
                    session_data['cart'] = cart
                    encoded_data = SessionStore().encode(session_data)
                    session.session_data = encoded_data
                    session.save()

        super(ProductAdmin, self).save_model(request, obj, form, change)


@admin.register(ImageItem)
class ImageItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'get_image',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" style="max-height: 250px""')

    get_image.short_description = 'Image'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'product', 'user', 'status', 'created', 'updated']
    readonly_fields = ('name', 'email', 'user', 'body', 'product', 'created', 'updated')
    list_editable = ['status']
    save_on_top = True

    fieldsets = (
        (None, {
            "fields": (('created', 'updated'), 'status')
        }),
        (None, {
            "fields": (('user', 'product',),)
        }),
        (None, {
            "fields": (('name', 'email',),)
        }),
        (None, {
            "fields": ('parent', 'body')
        }),

    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'rate', 'user', 'status', 'created', 'updated']
    readonly_fields = ('name', 'rate', 'user', 'product', 'created', 'updated')
    list_editable = ['status']
    save_on_top = True

    fieldsets = (
        (None, {
            "fields": (('created', 'updated'), 'status')
        }),
        (None, {
            "fields": (('user', 'product', 'rate',),)
        }),
        (None, {
            "fields": (('name',), 'advantages', 'disadvantages')
        }),
        (None, {
            "fields": ('body',)
        }),

    )
