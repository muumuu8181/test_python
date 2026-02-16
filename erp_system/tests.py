from django.test import TestCase
from sales.models import Customer, Product, Order, OrderItem
from inventory.models import Stock, StockMovement
from hr.models import Employee, Department, Position
from django.utils import timezone

class ERPTestCase(TestCase):
    def setUp(self):
        # 部署・役職・従業員
        self.dept = Department.objects.create(name="Sales", code="SALES")
        self.pos = Position.objects.create(title="Manager", rank=1)
        self.emp = Employee.objects.create(
            first_name="Taro", last_name="Yamada", email="taro@example.com",
            department=self.dept, position=self.pos, hire_date=timezone.now().date()
        )
        # 顧客・商品
        self.customer = Customer.objects.create(name="Client A", code="C001")
        self.product = Product.objects.create(name="Item A", code="P001", price=1000)

    def test_stock_movement(self):
        # 在庫移動のテスト
        StockMovement.objects.create(product=self.product, movement_type='in', quantity=10)
        stock = Stock.objects.get(product=self.product)
        self.assertEqual(stock.quantity, 10)

        StockMovement.objects.create(product=self.product, movement_type='out', quantity=3)
        stock.refresh_from_db()
        self.assertEqual(stock.quantity, 7)

    def test_order_total(self):
        # 受注金額の計算テスト
        order = Order.objects.create(customer=self.customer, employee=self.emp)
        item1 = OrderItem.objects.create(order=order, product=self.product, quantity=2) # 2000

        order.refresh_from_db()
        self.assertEqual(order.total_amount, 2000)

        item2 = OrderItem.objects.create(order=order, product=self.product, quantity=1) # +1000
        order.refresh_from_db()
        self.assertEqual(order.total_amount, 3000)
