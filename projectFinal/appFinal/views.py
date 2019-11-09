from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import User, Customer, LogedIn, Employee, Shop, Stock, Instock


def getIP(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    try:
        user = LogedIn.objects.get(loged_ip=ip).loged_user
    except:
        user = ''

    tmp = {'ip': ip, 'user': user}

    return tmp


def login(request):
    """
    歡迎畫面
    ------------------------
    讓使用者憑自己帳號登入
    ------------------------
    TODO: 帳密錯誤提示訊息
    """
    shopAll = Shop.objects.all()
    if request.session.get('is_login', None):  # 不允許重複登入，已登入者轉跳/app/index
        return redirect('/app/index')

    if 'loginB' in request.POST:  # 已提交了帳號密碼，開始進行確認
        userId = request.POST['userId']
        userPw = request.POST['userPw']
        userShop = request.POST['loginShop']

        try:  # 先進資料庫比對帳號
            user = User.objects.get(user_id=userId)
        except:  # 帳號比對失敗
            message = '帳號不存在'
            return render(request, 'login.html', locals())

        if user.user_pw == userPw:  # 帳號比對成功，開始進行密碼比對
            # 密碼比對成功，開始將使用者資料放進session
            request.session['is_login'] = True
            request.session['user_id'] = user.user_id
            request.session['user_emp_id'] = user.user_emp_id

            try:  # 將進當前店鋪資訊放進session
                request.session['user_shop'] = userShop
                request.session['user_shop_name'] = Shop.objects.get(
                    shop_id=userShop).shop_name
            except BaseException as e:
                print(e)

            try:  # 將employee中文名放進session
                employee = Employee.objects.get(emp_id=user.user_emp_id)
                request.session['emp_name_ch'] = employee.emp_name_ch
            except BaseException as e:
                print(e)

            return redirect('/app/index')

        else:  # 密碼錯誤
            message = '密碼錯誤'
            return render(request, 'login.html', locals())

    else:  # 未提交帳號密碼時，提供輸入框，並等待提交
        return render(request, 'login.html', locals())


def logout(request):

    if not request.session.get('is_login', None):  # 如果本來就沒登入
        return redirect('/app')

    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']

    return redirect('/app')


def index(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')

    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    return render(request, 'index.html', locals())


def changeShop(request, a):
    request.session['user_shop'] = a
    request.session['user_shop_name'] = Shop.objects.get(shop_id=a).shop_name

    return redirect('/app/index')


def cus(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    persMenuOpen = "active menu-open"

    cusAll = Customer.objects.all().exclude(cus_seeable=False)

    return render(request, 'cus.html', locals())


def addCus(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')

    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

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
        Customer.objects.create(cus_name=cusName, cus_name_en=cusEnName, cus_id=cusId, cus_class=cusClass, cus_idcard=cusIdCard, cus_sex=cusSex, cus_phone1=cusPhone1, cus_phone2=cusPhone2,
                                cus_addr1=cusAddr1, cus_addr2=cusAddr2, cus_email=cusEmail, cus_bd=cusBd, cus_shop_id="tmp", cus_arr_date=cusArrDate, cus_source="tmp", cus_remark=cusRemark)

        return redirect('/app/cus')
    return render(request, 'addCus.html', locals())


def editCus(request, a):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')

    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

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
        Customer.objects.filter(cus_id=a).update(cus_name=cusName, cus_name_en=cusEnName, cus_id=cusId, cus_class=cusClass, cus_idcard=cusIdCard, cus_sex=cusSex, cus_phone1=cusPhone1,
                                                 cus_phone2=cusPhone2, cus_addr1=cusAddr1, cus_addr2=cusAddr2, cus_email=cusEmail, cus_bd=cusBd, cus_shop_id="tmp", cus_arr_date=cusArrDate, cus_source="tmp", cus_remark=cusRemark)

        return redirect('/app/cus')

    if 'removeB' in request.POST:
        Customer.objects.filter(cus_id=a).update(cus_seeable=False)

        return redirect('/app/cus')

    return render(request, 'editCus.html', locals())


def removed(request, a):
    persMenuOpen = "active menu-open"

    if a == 'emp':
        type = '員工'
        typeValue = a
        removedAll = Employee.objects.filter(emp_seeable=False)
        for removed in removedAll:
            removed.name = removed.emp_name_ch
            removed.id = removed.emp_id
    if a == 'cus':
        type = '顧客'
        typeValue = a
        removedAll = Customer.objects.filter(cus_seeable=False)
        for removed in removedAll:
            removed.name = removed.cus_name
            removed.id = removed.cus_id
    return render(request, 'removed.html', locals())


def restore(request, a, b):
    if a == 'emp':
        Employee.objects.filter(emp_id=b).update(emp_seeable=True)
        return redirect('/app/removed/emp')

    if a == 'cus':
        Customer.objects.filter(cus_id=b).update(cus_seeable=True)
        return redirect('/app/removed/cus')


def delete(request, a, b):
    if a == 'emp':
        Employee.objects.get(emp_id=b).delete()
        return redirect('/app/removed/emp')

    if a == 'cus':
        Customer.objects.get(cus_id=b).delete()
        return redirect('/app/removed/cus')


def emp(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    persMenuOpen = "active menu-open"

    empAll = Employee.objects.all().exclude(emp_seeable=False)

    return render(request, 'emp.html', locals())


def addEmp(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    persMenuOpen = "active menu-open"

    if 'saveB' in request.POST:
        empName = request.POST['empName']
        empEnName = request.POST['empEnName']
        empId = request.POST['empId']
        empClass = request.POST['empClass']
        empIdCard = request.POST['empIdCard']
        empSalary = request.POST['empSalary']
        empBd = request.POST['empBd']
        empArrDate = request.POST['empArrDate']
        empLeaveDate = request.POST['empLeaveDate']
        empPhone1 = request.POST['empPhone1']
        empPhone2 = request.POST['empPhone2']
        empAddr1 = request.POST['empAddr1']
        empAddr2 = request.POST['empAddr2']
        empEmail = request.POST['empEmail']
        empRemark = request.POST['empRemark']
        Employee.objects.create(emp_name_ch=empName, emp_name_en=empEnName, emp_id=empId, emp_class=empClass, emp_idcard=empIdCard, emp_salary=empSalary, emp_phone1=empPhone1, emp_phone2=empPhone2,
                                emp_addr1=empAddr1, emp_addr2=empAddr2, emp_email=empEmail, emp_bd=empBd, emp_shop_id="tmp", emp_arr_date=empArrDate, emp_leave_date=empLeaveDate, emp_remark=empRemark)

        return redirect('/app/emp')
    return render(request, 'addEmp.html', locals())


def editEmp(request, a):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    persMenuOpen = "active menu-open"

    empThis = Employee.objects.get(emp_id=a)

    empThisClassOther = ['頭皮護理師', '資深設計師', '設計師', '助理']
    if empThis.emp_class == '頭皮護理師':
        empThisClass = '頭皮護理師'
        empThisClassOther.remove('頭皮護理師')
    elif empThis.emp_class == '資深設計師':
        empThisClass = '資深設計師'
        empThisClassOther.remove('資深設計師')
    elif empThis.emp_class == '設計師':
        empThisClass = '設計師'
        empThisClassOther.remove('設計師')
    elif empThis.emp_class == '助理':
        empThisClass = '助理'
        empThisClassOther.remove('助理')
    else:
        empThisClass = "---"

    if 'saveB' in request.POST:
        empName = request.POST['empName']
        empEnName = request.POST['empEnName']
        empId = request.POST['empId']
        empClass = request.POST['empClass']
        empIdCard = request.POST['empIdCard']
        empSalary = request.POST['empSalary']
        empBd = request.POST['empBd']
        empArrDate = request.POST['empArrDate']
        empLeaveDate = request.POST['empLeaveDate']
        empPhone1 = request.POST['empPhone1']
        empPhone2 = request.POST['empPhone2']
        empAddr1 = request.POST['empAddr1']
        empAddr2 = request.POST['empAddr2']
        empEmail = request.POST['empEmail']
        empRemark = request.POST['empRemark']
        Employee.objects.filter(emp_id=a).update(emp_name_ch=empName, emp_name_en=empEnName, emp_id=empId, emp_class=empClass, emp_idcard=empIdCard, emp_salary=empSalary, emp_phone1=empPhone1,
                                                 emp_phone2=empPhone2, emp_addr1=empAddr1, emp_addr2=empAddr2, emp_email=empEmail, emp_bd=empBd, emp_shop_id="tmp", emp_arr_date=empArrDate, emp_leave_date=empLeaveDate, emp_remark=empRemark)

        return redirect('/app/emp')

    if 'removeB' in request.POST:
        Employee.objects.filter(emp_id=a).update(emp_seeable=False)
        return redirect('/app/emp')

    return render(request, 'editEmp.html', locals())


def stock(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    stockMenuOpen = "active menu-open"
    
    stockAll = Stock.objects.all()

    for stock in stockAll:
        stock.instock_qua = Instock.objects.get(instock_id=stock.stock_id, insock_shop_id=request.session['user_shop']).instock_qua

    return render(request, 'stock.html', locals())


def sale(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    saleMenuOpen = "active menu-open"
    return render(request, 'sale.html', locals())


def service(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    saleMenuOpen = "active menu-open"
    return render(request, 'service.html', locals())


def addStock(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    stockMenuOpen = "active menu-open"

    if 'saveB' in request.POST:
        stock_type = request.POST['stock_type']
        stock_id = request.POST['stock_id']
        stock_name = request.POST['stock_name']
        stock_price = request.POST['stock_price']
        stock_cost = request.POST['stock_cost']
        stock_point = request.POST['stock_point']
        stock_remark = request.POST['stock_remark']

        Stock.objects.create(stock_type=stock_type, stock_id=stock_id, stock_name=stock_name,
                            stock_price=stock_price, stock_cost=stock_cost, stock_point=stock_point, stock_remark=stock_remark)
        
        for shop in shopAll:
            Instock.objects.create(instock_id=stock_id, insock_shop_id=shop.shop_id, instock_qua=0, instock_salesvolume=0)

        return redirect('/app/stock')


    return render(request, 'addStock.html', locals())


def deduct(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    saleMenuOpen = "active menu-open"
    return render(request, 'deduct.html', locals())


def exportStock(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    stockMenuOpen = "active menu-open"
    return render(request, 'exportStock.html', locals())


def importStock(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    stockMenuOpen = "active menu-open"

    stockAll = Stock.objects.all()
    for stock in stockAll:
        stock.instock_qua = Instock.objects.get(instock_id=stock.stock_id, insock_shop_id=request.session['user_shop']).instock_qua

    return render(request, 'importStock.html', locals())

# def selectImport(request):
#     if not request.session.get('is_login', None):  # 確認是否登入
#     return redirect('/app')
#     userNow = request.session['emp_name_ch']
#     shopNow = request.session['user_shop_name']
#     shopAll = Shop.objects.all()

#     stockMenuOpen = "active menu-open"

#     stockAll = Stock.objects.all()
#     for stock in stockAll:
#         stock.instock_qua = Instock.objects.get(instock_id=stock.stock_id, insock_shop_id=request.session['user_shop']).instock_qua

#     return redirect('/app/import/')



def report(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    reportMenuOpen = "active menu-open"
    return render(request, 'report.html', locals())


def salaryCount(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    reportMenuOpen = "active menu-open"
    return render(request, 'salaryCount.html', locals())


def turnoverCount(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    reportMenuOpen = "active menu-open"
    return render(request, 'turnoverCount.html', locals())


def setting(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    return render(request, 'setting.html', locals())


def setShop(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    return render(request, 'setShop.html', locals())


def addShop(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    if 'saveB' in request.POST:
        shop_name = request.POST['shop_name']
        shop_id = request.POST['shop_id']
        shop_class = request.POST['shop_class']
        shop_addr = request.POST['shop_addr']
        shop_phone1 = request.POST['shop_phone1']
        shop_phone2 = request.POST['shop_phone2']
        shop_remark = request.POST['shop_remark']

        Shop.objects.create(shop_name=shop_name, shop_id=shop_id, shop_class=shop_class, shop_addr=shop_addr,
                            shop_phone1=shop_phone1, shop_phone2=shop_phone2, shop_remark=shop_remark)

        stockAll = Stock.objects.all()
        for stock in stockAll:
            Instock.objects.create(instock_id=stock.stock_id, insock_shop_id=request.session['user_shop'], instock_qua=0, instock_salesvolume=0)

        return redirect('/app/setting/shop')

    return render(request, 'addShop.html', locals())


def ok(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()
    return render(request, 'ok.html', locals())
