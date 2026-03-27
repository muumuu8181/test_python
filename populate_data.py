import os
import django
from django.utils import timezone
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from core.models import CompanyInfo
from hr.models import Department, Position, Employee
from sales.models import Customer, Product, Order, OrderItem
from inventory.models import StockMovement

def populate():
    print("Creating Company Info...")
    CompanyInfo.objects.get_or_create(
        name="株式会社ERPデモ",
        address="東京都千代田区1-1-1",
        phone="03-1234-5678",
        email="info@erp-demo.co.jp",
        website="https://www.erp-demo.co.jp"
    )

    print("Creating Departments...")
    sales_dept, _ = Department.objects.get_or_create(name="営業部", code="SALES")
    dev_dept, _ = Department.objects.get_or_create(name="開発部", code="DEV")
    admin_dept, _ = Department.objects.get_or_create(name="総務部", code="ADMIN")

    print("Creating Positions...")
    manager_pos, _ = Position.objects.get_or_create(title="部長", rank=10)
    leader_pos, _ = Position.objects.get_or_create(title="課長", rank=20)
    staff_pos, _ = Position.objects.get_or_create(title="社員", rank=30)

    print("Creating Employees...")
    emp1, _ = Employee.objects.get_or_create(
        email="yamada@erp-demo.co.jp",
        defaults={
            "first_name": "太郎", "last_name": "山田",
            "phone": "090-1111-2222",
            "department": sales_dept, "position": manager_pos,
            "hire_date": timezone.now().date()
        }
    )
    emp2, _ = Employee.objects.get_or_create(
        email="suzuki@erp-demo.co.jp",
        defaults={
            "first_name": "次郎", "last_name": "鈴木",
            "phone": "090-3333-4444",
            "department": dev_dept, "position": staff_pos,
            "hire_date": timezone.now().date()
        }
    )

    print("Creating Customers...")
    cust1, _ = Customer.objects.get_or_create(
        code="C001",
        defaults={
            "name": "株式会社A", "email": "contact@a-corp.co.jp",
            "phone": "03-5555-6666", "address": "東京都港区"
        }
    )
    cust2, _ = Customer.objects.get_or_create(
        code="C002",
        defaults={
            "name": "合同会社B", "email": "info@b-llc.co.jp",
            "phone": "06-7777-8888", "address": "大阪府大阪市"
        }
    )

    print("Creating Products...")
    prod1, _ = Product.objects.get_or_create(
        code="P001",
        defaults={"name": "高性能PC", "price": Decimal("150000"), "description": "ハイスペックなデスクトップPC"}
    )
    prod2, _ = Product.objects.get_or_create(
        code="P002",
        defaults={"name": "オフィスチェア", "price": Decimal("30000"), "description": "長時間座っても疲れない椅子"}
    )

    print("Creating Stock Movements (Initial Inventory)...")
    # P001: 10個入荷
    StockMovement.objects.create(product=prod1, movement_type='in', quantity=10, note="初期在庫")
    # P002: 20個入荷
    StockMovement.objects.create(product=prod2, movement_type='in', quantity=20, note="初期在庫")

    print("Creating Orders...")
    order1 = Order.objects.create(customer=cust1, employee=emp1, status='ordered')
    OrderItem.objects.create(order=order1, product=prod1, quantity=2)
    OrderItem.objects.create(order=order1, product=prod2, quantity=5)

    print("Data population completed successfully!")

if __name__ == '__main__':
    populate()
