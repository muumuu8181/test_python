from django.shortcuts import render
from sales.models import Order
from inventory.models import Stock

def index(request):
    # 簡易ダッシュボード用のデータ取得
    order_count = Order.objects.count()
    low_stock_items = Stock.objects.filter(quantity__lt=10)

    context = {
        'order_count': order_count,
        'low_stock_items': low_stock_items,
    }
    return render(request, 'core/index.html', context)
