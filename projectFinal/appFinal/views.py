from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import User, Customer, LogedIn

def getIP(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    try:
        user = LogedIn.objects.get(loged_ip=ip).loged_user
    except:
        user=''
    
    tmp = {'ip':ip, 'user':user}

    return tmp

def login(request):
    if 'loginB' in request.POST:
        userId = request.POST['userId']
        userPw = request.POST['userPw']
        try:
            User.objects.get(user_id=userId, user_pw=userPw)
            userNow = userId

            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip =  request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']

            LogedIn.objects.get_or_create(loged_user=userId, loged_ip=ip)

            return redirect('/app/index')
        except:
            return redirect('/app')

    return render(request, 'login.html', locals())

def logout(request, a):
    LogedIn.objects.filter(loged_user=a).delete()
    return redirect('/app')

def index(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')

    return render(request, 'index.html', locals())

def cus(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
    persMenuOpen = "active menu-open"

    cusAll = Customer.objects.all().exclude(cus_seeable='0')

    return render(request, 'cus.html', locals())

def addCus(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
    persMenuOpen = "active menu-open"
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
        Customer.objects.create(cus_name=cusName, cus_name_en=cusEnName, cus_id=cusId, cus_class=cusClass, cus_idcard=cusIdCard, cus_sex=cusSex, cus_phone1=cusPhone1, cus_phone2=cusPhone2, cus_addr1=cusAddr1, cus_addr2=cusAddr2, cus_email=cusEmail, cus_bd=cusBd, cus_shop_id="tmp", cus_arr_date=cusArrDate, cus_source="tmp", cus_remark=cusRemark)
    
        return redirect('/app/cus')
    return render(request, 'addCus.html', locals())

def editCus(request, a):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
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
    if cusThis.cus_class == '3':
        cusThisClass = '金'
        cusThisClassOther.append(('銅', '1'))
        cusThisClassOther.append(('銀', '2'))
    elif cusThis.cus_class == '2':
        cusThisClass = '銀'
        cusThisClassOther.append(('銅', '1'))
        cusThisClassOther.append(('金', '3'))
    elif cusThis.cus_class == '1':
        cusThisClass = '銅'
        cusThisClassOther.append(('銀', '2'))
        cusThisClassOther.append(('金', '3'))
    else:
        cusThisClass = "---"
        cusThisClassOther.append(('銅', '1'))
        cusThisClassOther.append(('銀', '2'))
        cusThisClassOther.append(('金', '3'))

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
        
        return redirect('/app/cus')

    if 'removeB' in request.POST:
        Customer.objects.filter(cus_id=a).update(cus_seeable='0')

        return redirect('/app/cus')       

    return render(request, 'editCus.html', locals())

def removedCus(request):
    persMenuOpen = "active menu-open"
    removedAll = Customer.objects.filter(cus_seeable='0')
    return render(request, 'removedCus.html', locals())

def restoreCus(request, a):
    Customer.objects.filter(cus_id=a).update(cus_seeable='1')

    return redirect('/app/removedCus')    

def deleteCus(request, a):

    Customer.objects.get(cus_id=a).delete()

    return redirect('/app/removedCus')    

def emp(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
    persMenuOpen = "active menu-open"
    return render(request, 'emp.html', locals())

def stock(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
    stockMenuOpen = "active menu-open"
    return render(request, 'stock.html', locals())

def sale(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
    saleMenuOpen = "active menu-open"
    return render(request, 'sale.html', locals())

def service(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
    saleMenuOpen = "active menu-open"
    return render(request, 'service.html', locals())

def addStock(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
    stockMenuOpen = "active menu-open"
    return render(request, 'addStock.html', locals())

def deduct(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
    saleMenuOpen = "active menu-open"
    return render(request, 'deduct.html', locals())

def exportStock(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
    stockMenuOpen = "active menu-open"
    return render(request, 'exportStock.html', locals())

def importStock(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
    stockMenuOpen = "active menu-open"
    return render(request, 'importStock.html', locals())

def report(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
    reportMenuOpen = "active menu-open"
    return render(request, 'report.html', locals())

def salaryCount(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
    reportMenuOpen = "active menu-open"
    return render(request, 'salaryCount.html', locals())

def turnoverCount(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
    reportMenuOpen = "active menu-open"
    return render(request, 'turnoverCount.html', locals())

def setting(request):
    userNow = getIP(request)
    if not LogedIn.objects.filter(loged_ip=userNow['ip']):
        return redirect('/app')
    return render(request, 'setting.html', locals())