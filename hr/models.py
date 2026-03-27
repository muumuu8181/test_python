from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="部署名")
    code = models.CharField(max_length=20, unique=True, verbose_name="部署コード")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name="親部署")

    class Meta:
        verbose_name = "部署"
        verbose_name_plural = "部署"

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=100, verbose_name="役職名")
    rank = models.IntegerField(default=0, verbose_name="ランク")

    class Meta:
        verbose_name = "役職"
        verbose_name_plural = "役職"
        ordering = ['rank']

    def __str__(self):
        return self.title

class Employee(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="名")
    last_name = models.CharField(max_length=50, verbose_name="姓")
    email = models.EmailField(unique=True, verbose_name="メールアドレス")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="電話番号")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="部署")
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="役職")
    hire_date = models.DateField(verbose_name="入社日")
    is_active = models.BooleanField(default=True, verbose_name="在籍中")

    class Meta:
        verbose_name = "従業員"
        verbose_name_plural = "従業員"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
