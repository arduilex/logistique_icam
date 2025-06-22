from django.contrib import admin
from .models import Product, Order, OrderItem, Transaction


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'reference', 'quantity', 'price', 'is_low_stock', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'reference']
    readonly_fields = ['created_at', 'updated_at']
    
    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Stock faible'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'order_type', 'status', 'order_date', 'supplier_customer']
    list_filter = ['order_type', 'status', 'order_date']
    search_fields = ['order_number', 'supplier_customer']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['product', 'transaction_type', 'quantity', 'unit_price', 'timestamp']
    list_filter = ['transaction_type', 'timestamp']
    search_fields = ['product__name', 'product__reference']
    readonly_fields = ['timestamp']