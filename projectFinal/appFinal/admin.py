from django.contrib import admin
from .models import User, Customer, LogedIn, Employee, Shop, Stock, Instock, ImportReport, ImportStock

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


admin.site.register(User)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(LogedIn)
admin.site.register(Employee)
admin.site.register(Shop)
admin.site.register(Stock, StockAdmin)
admin.site.register(Instock)
admin.site.register(ImportReport)
admin.site.register(ImportStock)
