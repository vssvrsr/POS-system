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