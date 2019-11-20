from django.urls import path
from appFinal import views as appViews

app_name = 'appFinal'

urlpatterns = [
    # 登入登出
    path('', appViews.login, name='login'),
    path('logout/', appViews.logout, name='logout'),
    path('index/', appViews.index, name='index'),
    path('changeShop/<str:a>', appViews.changeShop, name='changeShop'),


    # 人員管理
    path('cus/', appViews.cus, name='cus'),
    path('addCus/', appViews.addCus, name='addCus'),
    path('editCus/<str:a>', appViews.editCus, name='editCus'),

    path('emp/', appViews.emp, name='emp'),
    path('addEmp/', appViews.addEmp, name='addEmp'),
    path('editEmp/<str:a>', appViews.editEmp, name='editEmp'),

    path('removed/<str:a>', appViews.removed, name='removed'),
    path('restore/<str:a>/<str:b>', appViews.restore, name='restoreCus'),
    path('delete/<str:a>/<str:b>', appViews.delete, name='deleteCus'),


    # 前台交易
    path('sale/', appViews.sale, name='sale'),
    path('sale/next', appViews.saleNext, name='saleNext'),
    path('selectSale/<str:a>/<str:b>', appViews.selectSale, name='selectSale'),
    path('saleLog/', appViews.saleLog, name='saleLog'),


    path('service/', appViews.service, name='service'),
    path('deduct/', appViews.deduct, name='deduct'),




    path('stock/', appViews.stock, name='stock'),
    path('addStock/', appViews.addStock, name='addStock'),
    path('editStock/<str:row_index>', appViews.editStock, name='editStock'),
    path('importStock/', appViews.importStock, name='importStock'),
    path('selectImport/<str:a>/<str:b>',
         appViews.selectImport, name='selectImport'),
    path('exportStock/', appViews.exportStock, name='exportStock'),

    # 報表結算
    path('stockReport/', appViews.stockReport, name='stockReport'),
    path('salaryCount/', appViews.salaryCount, name='salaryCount'),
    path('turnoverCount/', appViews.turnoverCount, name='turnoverCount'),

    path('setting/', appViews.setting, name='setting'),
    path('setting/shop', appViews.setShop, name='setShop'),
    path('setting/addShop', appViews.addShop, name='addShop'),

    path('selectPerson/<str:a>/<str:b>/<str:c>',
         appViews.selectPerson, name='selectPerson'),

    path('ok', appViews.ok, name='ok'),
]
