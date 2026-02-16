from django.contrib import admin
from .models import Department, Position, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent')
    search_fields = ('name', 'code')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'rank')
    ordering = ('rank',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'department', 'position', 'email', 'phone', 'hire_date', 'is_active')
    list_filter = ('department', 'position', 'is_active', 'hire_date')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    ordering = ('department', 'position', 'last_name', 'first_name')
