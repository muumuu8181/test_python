from django.db import models
from sales.models import Product

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock', verbose_name="商品")
    quantity = models.IntegerField(default=0, verbose_name="在庫数")
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="保管場所")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "在庫"
        verbose_name_plural = "在庫"

    def __str__(self):
        return f"{self.product.name}: {self.quantity}"

class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = (
        ('in', '入荷 (+)'),
        ('out', '出荷 (-)'),
        ('return', '返品受入 (+)'),
        ('waste', '廃棄 (-)'),
        ('adjust_in', '調整増 (+)'),
        ('adjust_out', '調整減 (-)'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements', verbose_name="商品")
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES, verbose_name="移動タイプ")
    quantity = models.PositiveIntegerField(verbose_name="数量")
    date = models.DateTimeField(auto_now_add=True, verbose_name="日時")
    note = models.TextField(blank=True, null=True, verbose_name="備考")

    class Meta:
        verbose_name = "入出庫履歴"
        verbose_name_plural = "入出庫履歴"
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        # 新規作成時のみ在庫を更新
        if self.pk is None:
            stock, created = Stock.objects.get_or_create(product=self.product)

            if self.movement_type in ['in', 'return', 'adjust_in']:
                stock.quantity += self.quantity
            elif self.movement_type in ['out', 'waste', 'adjust_out']:
                stock.quantity -= self.quantity

            stock.save()

        super().save(*args, **kwargs)
