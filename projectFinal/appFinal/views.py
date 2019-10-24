from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import User, Customer

def login(request):
    if 'loginB' in request.POST:
        userId = request.POST['userId']
        userPw = request.POST['userPw']
        try:
            User.objects.get(user_id=userId, user_pw=userPw)
            return HttpResponse('登入成功')
        except:
            return HttpResponse('登入失敗')

    return render(request, 'login.html', locals())

def index(request):
    return render(request, 'index.html', locals())

def cus(request):
    persMenuOpen = "active menu-open"

    cusAll = Customer.objects.all()

    return render(request, 'cus.html', locals())

def addCus(request):
    persMenuOpen = "active menu-open"
    if 'saveB' in request.POST:
        cusName = request.POST['cusName']
        cusEnName = request.POST['cusEnName']
        cusId = request.POST['cusName']
        cusClass = request.POST['cusClass']
        cusIdCard = request.POST['cusIdCard']
        cusSex = request.POST['cusSex']
        cusBd = request.POST['cusBd']
        cusArrDate = request.POST['cusArrDate']
        cusPhone1 = request.POST['cusPhone1']
        cusPhone2 = request.POST['cusPhone2']
        cusAddr1 = request.POST['cusAddr1']
        cusAddr2 = request.POST['cusAddr2']
        cusEmail = request.POST['cusEmail']
        cusRemark = request.POST['cusRemark']

        Customer.objects.create(cus_name=cusName, cus_name_en=cusEnName, cus_id=cusId, cus_class=cusClass, cus_idcard=cusIdCard, cus_sex=cusSex, cus_phone1=cusPhone1, cus_phone2=cusPhone2, cus_addr1=cusAddr1, cus_addr2=cusAddr2, cus_email=cusEmail, cus_bd=cusBd, cus_shop_id="tmp", cus_arr_date=cusArrDate, cus_source="tmp", cus_remark=cusRemark)
    return render(request, 'addCus.html', locals())

def editCus(request, a):
    persMenuOpen = "active menu-open"
    cusThis = Customer.objects.get(cus_id=a)

    if cusThis.cus_sex == 'M':
        cusThisSex = '男'
        otherSexValue = 'F'
        otherSex = '女'
    else:
        cusThisSex = '女'
        otherSexValue = 'M'
        otherSex = '男'

    cusThisClassOther = []
    cusThisClassOtherValue = []
    if cusThis.cus_class == '3':
        cusThisClass = '金'
        cusThisClassOther.append('銅').append('銀')
        cusThisClassOtherValue.append('1').append('2')
    elif cusThis.cus_class == '2':
        cusThisClass = '銀'
        cusThisClassOther.append('銅').append('金')
        cusThisClassOtherValue.append('1').append('3')
    elif cusThis.cus_class == '1':
        cusThisClass = '銅'
        cusThisClassOther.append('銀').append('金')
        cusThisClassOtherValue.append('2').append('3')

    if 'saveB' in request.POST:
        cusName = request.POST['cusName']
        cusEnName = request.POST['cusEnName']
        cusId = request.POST['cusId']
        cusClass = request.POST['cusClass']
        cusIdCard = request.POST['cusIdCard']
        cusSex = request.POST['cusSex']
        cusBd = request.POST['cusBd']
        cusArrDate = request.POST['cusArrDate']
        cusPhone1 = request.POST['cusPhone1']
        cusPhone2 = request.POST['cusPhone2']
        cusAddr1 = request.POST['cusAddr1']
        cusAddr2 = request.POST['cusAddr2']
        cusEmail = request.POST['cusEmail']
        cusRemark = request.POST['cusRemark']
        Customer.objects.filter(cus_id=a).update(cus_name=cusName, cus_name_en=cusEnName, cus_id=cusId, cus_class=cusClass, cus_idcard=cusIdCard, cus_sex=cusSex, cus_phone1=cusPhone1, cus_phone2=cusPhone2, cus_addr1=cusAddr1, cus_addr2=cusAddr2, cus_email=cusEmail, cus_bd=cusBd, cus_shop_id="tmp", cus_arr_date=cusArrDate, cus_source="tmp", cus_remark=cusRemark)

    return render(request, 'editCus.html', locals())

def emp(request):
    persMenuOpen = "active menu-open"
    return render(request, 'emp.html', locals())

def stock(request):
    stockMenuOpen = "active menu-open"
    return render(request, 'stock.html', locals())

def sale(request):
    saleMenuOpen = "active menu-open"
    return render(request, 'sale.html', locals())

def service(request):
    saleMenuOpen = "active menu-open"
    return render(request, 'service.html', locals())

def addStock(request):
    stockMenuOpen = "active menu-open"
    return render(request, 'addStock.html', locals())

def deduct(request):
    saleMenuOpen = "active menu-open"
    return render(request, 'deduct.html', locals())

def exportStock(request):
    stockMenuOpen = "active menu-open"
    return render(request, 'exportStock.html', locals())

def importStock(request):
    stockMenuOpen = "active menu-open"
    return render(request, 'importStock.html', locals())

def report(request):
    reportMenuOpen = "active menu-open"
    return render(request, 'report.html', locals())

def salaryCount(request):
    reportMenuOpen = "active menu-open"
    return render(request, 'salaryCount.html', locals())

def turnoverCount(request):
    reportMenuOpen = "active menu-open"
    return render(request, 'turnoverCount.html', locals())

def setting(request):
    return render(request, 'setting.html', locals())