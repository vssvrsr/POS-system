from django.contrib import admin
from .models import User, Customer, LogedIn, Employee, Shop, Stock, Instock

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class CustomerResource(resources.ModelResource):

    class Meta:
        model = Customer

class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource

admin.site.register(User)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(LogedIn)
admin.site.register(Employee)
admin.site.register(Shop)
admin.site.register(Stock)
admin.site.register(Instock)