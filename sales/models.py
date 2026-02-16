from django.db import models
from hr.models import Employee

class Customer(models.Model):
    name = models.CharField(max_length=255, verbose_name="顧客名")
    code = models.CharField(max_length=50, unique=True, verbose_name="顧客コード")
    email = models.EmailField(blank=True, null=True, verbose_name="メールアドレス")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="電話番号")
    address = models.TextField(blank=True, null=True, verbose_name="住所")

    class Meta:
        verbose_name = "顧客"
        verbose_name_plural = "顧客"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="商品名")
    code = models.CharField(max_length=50, unique=True, verbose_name="商品コード")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="単価")
    description = models.TextField(blank=True, null=True, verbose_name="説明")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('estimate', '見積'),
        ('ordered', '受注'),
        ('shipped', '出荷済'),
        ('billed', '請求済'),
        ('paid', '入金済'),
        ('cancelled', 'キャンセル'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="顧客")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="担当者")
    order_date = models.DateField(auto_now_add=True, verbose_name="受注日")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="合計金額")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='estimate', verbose_name="ステータス")

    class Meta:
        verbose_name = "受注"
        verbose_name_plural = "受注"

    def __str__(self):
        return f"{self.customer} - {self.order_date}"

    def calculate_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="受注")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="商品")
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="単価")

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    class Meta:
        verbose_name = "受注明細"
        verbose_name_plural = "受注明細"

    def save(self, *args, **kwargs):
        if not self.unit_price and self.product:
            self.unit_price = self.product.price
        super().save(*args, **kwargs)
        # 親の合計金額を更新
        self.order.calculate_total()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        order.calculate_total()
