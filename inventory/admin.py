from django.contrib import admin
from .models import Stock, StockMovement

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'location', 'updated_at')
    search_fields = ('product__name', 'product__code', 'location')
    list_filter = ('updated_at', 'location')

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'date', 'note')
    search_fields = ('product__name', 'product__code')
    list_filter = ('movement_type', 'date')
    date_hierarchy = 'date'
