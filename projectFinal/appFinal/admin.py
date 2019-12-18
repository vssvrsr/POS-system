from django.contrib import admin
from .models import User, Customer, LogedIn, Employee, Shop, Stock, Instock, ImportReport, ImportStock, Sale, Salestock, Salealloc, Service, CustomerClass, RegularBonus, Commission, CustomerClass, CommLimit, MultiSevicePercent, SalarySelectEmp, SalaryResult, CommIncomeType
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# 引入import_export功能(https://django-import-export.readthedocs.io/en/latest/)
class CustomerResource(resources.ModelResource):

    class Meta:
        model = Customer


class StockResource(resources.ModelResource):

    class Meta:
        model = Stock


# 在Admin中顯示批次操作UI
class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource


class StockAdmin(ImportExportModelAdmin):
    resource_class = StockResource

# 選擇要顯示的欄位


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'emp_name_ch', 'emp_shop_id',
                    'emp_salary', 'emp_arr_date')

class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'serv_id',
        'serv_stock',
        'serv_emp1',
        'serv_emp2',
        'serv_emp3',
        'serv_stock_price',
        'serv_price',
        'serv_point'
    )

class SaleAlloc(admin.ModelAdmin):
    list_display = (
        'salealloc_sale',
        'salealloc_emp',
        'salealloc_perc'
    )


admin.site.register(User)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(LogedIn)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Shop)
admin.site.register(Stock, StockAdmin)
admin.site.register(Instock)
admin.site.register(ImportReport)
admin.site.register(ImportStock)
admin.site.register(Sale)
admin.site.register(Salestock)
admin.site.register(Salealloc, SaleAlloc)
admin.site.register(Service, ServiceAdmin)
admin.site.register(RegularBonus)
admin.site.register(Commission)
admin.site.register(CustomerClass)
admin.site.register(CommLimit)
admin.site.register(MultiSevicePercent)
admin.site.register(SalarySelectEmp)
admin.site.register(SalaryResult)
admin.site.register(CommIncomeType)
