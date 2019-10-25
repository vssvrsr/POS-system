from django.urls import path
from appFinal import views as appViews

app_name = 'appFinal'

urlpatterns = [
    path('', appViews.login),
    path('logout/<str:a>', appViews.logout, name='logout'),
    path('index/', appViews.index, name='index'),

    path('cus/', appViews.cus, name='cus'),
    path('addCus/', appViews.addCus, name='addCus'),
    path('editCus/<str:a>', appViews.editCus, name='editCus'),
    path('removedCus/', appViews.removedCus, name='removedCus'),
    path('restoreCus/<str:a>', appViews.restoreCus, name='restoreCus'),
    path('deleteCus/<str:a>', appViews.deleteCus, name='deleteCus'),

    path('emp/', appViews.emp, name='emp'),
    path('sale/', appViews.sale, name='sale'),
    path('service/', appViews.service, name='service'),
    path('deduct/', appViews.deduct, name='deduct'),
    path('report/', appViews.report, name='report'),
    path('addStock/', appViews.addStock, name='addStock'),
    path('stock/', appViews.stock, name='stock'),
    path('importStock/', appViews.importStock, name='importStock'),
    path('exportStock/', appViews.exportStock, name='exportStock'),
    path('salaryCount/', appViews.salaryCount, name='salaryCount'),
    path('turnoverCount/', appViews.turnoverCount, name='turnoverCount'),
    path('setting/', appViews.setting, name='setting'),
]
