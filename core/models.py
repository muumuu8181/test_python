from django.db import models

class CompanyInfo(models.Model):
    name = models.CharField(max_length=255, verbose_name="会社名")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="住所")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="電話番号")
    email = models.EmailField(null=True, blank=True, verbose_name="代表メールアドレス")
    website = models.URLField(null=True, blank=True, verbose_name="ウェブサイト")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "会社情報"
        verbose_name_plural = "会社情報"

    def __str__(self):
        return self.name
