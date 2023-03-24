from django.contrib import admin
from orders.models import OrderItem, Order, Delivery


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_first_name', 'customer_last_name', 'customer_email',
                    'status', 'city', 'address', 'paid', 'created', 'updated', 'available']
    list_filter = ['paid', 'created', 'updated', 'status']
    list_editable = ['paid', 'status', 'available']
    readonly_fields = ('order_id', 'customer_email', 'customer_phone', 'user',
                       'recipient_email', 'created', 'updated')
    search_fields = ('order_id', 'customer_last_name')
    save_on_top = True
    inlines = [OrderItemInline]

    fieldsets = (
        (None, {
            "fields": (('order_id', 'status', 'paid', 'available'), ('created', 'updated'),)
        }),
        ('Customer', {
            "fields": (('customer_first_name', 'customer_last_name', 'user'),
                       ('customer_phone', 'customer_email'),)
        }),
        ('Address', {
            "fields": (('city', 'address'),)
        }),
        ('Delivery & Payment', {
            "fields": (('delivery', 'paymentMethod',),)
        }),
        ('Recipient', {
            "fields": (('recipient_first_name', 'recipient_last_name', 'recipient_email'),)
        }),
        (None, {
            "fields": (('coupon', 'discount'),)
        }),
    )


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price']
    list_editable = ['price']