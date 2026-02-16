from django.contrib import admin
from .models import Customer, Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'phone', 'email')
    search_fields = ('name', 'code')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price')
    search_fields = ('name', 'code')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order_date', 'employee', 'total_amount', 'status')
    list_filter = ('status', 'order_date', 'employee')
    search_fields = ('customer__name', 'order_date')
    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # 合計金額の再計算（インラインアイテム変更時などに備えて）
        # ただし、OrderItemの保存は親の保存後に行われるため、ここでの計算は少しタイミングが難しい場合がある
        # 今回はOrderItemのsaveメソッドで親を更新するようにしているので、ここでは特に何もしなくてよい
        pass
