from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms
from django.contrib.admin import SimpleListFilter
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin

from store.models import *


"""@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}"""


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
    list_display = ['name', 'category', 'company', 'price', 'stock', 'sales', 'available', 'created', 'updated', 'get_image']
    list_filter = ['category', 'company', 'year', 'available', 'created', 'updated']
    readonly_fields = ('get_image', 'sales')
    search_fields = ('name', 'category__name', 'company__name')
    list_editable = ['price', 'stock', 'available']
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
            "fields": ('stock', 'available')
        }),
    )

    def get_image(self, obj):
        if obj.image.url:
            pass
        else:
            return mark_safe(f'<img src= width="100" style="max-height: 250px"')
        return mark_safe(f'<img src={obj.image.url} width="100" style="max-height: 250px"')

    get_image.short_description = 'Image'


@admin.register(ImageItem)
class ImageItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'get_image',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" style="max-height: 250px""')

    get_image.short_description = 'Image'