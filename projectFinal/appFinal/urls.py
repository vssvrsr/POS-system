from django.urls import path
from appFinal import views as appViews

app_name = 'appFinal'

urlpatterns = [
    path('', appViews.login, name='login'),
    path('logout/', appViews.logout, name='logout'),
    path('index/', appViews.index, name='index'),
    path('changeShop/<str:a>', appViews.changeShop, name='changeShop'),

    path('cus/', appViews.cus, name='cus'),
    path('addCus/', appViews.addCus, name='addCus'),
    path('editCus/<str:a>', appViews.editCus, name='editCus'),

    path('emp/', appViews.emp, name='emp'),
    path('addEmp/', appViews.addEmp, name='addEmp'),
    path('editEmp/<str:a>', appViews.editEmp, name='editEmp'),

    path('removed/<str:a>', appViews.removed, name='removed'),
    path('restore/<str:a>/<str:b>', appViews.restore, name='restoreCus'),
    path('delete/<str:a>/<str:b>', appViews.delete, name='deleteCus'),

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
    path('setting/shop', appViews.setShop, name='setShop'),
    path('setting/addShop', appViews.addShop, name='addShop'),
]
