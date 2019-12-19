from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import User, Customer, LogedIn, Employee, Shop, Stock, Instock, ImportReport, ImportStock, Sale, Salestock, Salealloc, Service, CustomerClass, RegularBonus, Commission, CustomerClass, CommLimit, MultiSevicePercent, SalarySelectEmp, SalaryResult, CommIncomeType
from chat.models import Message

"""
    登入、登出、切換分店相關系統
    ------------------------
    讓使用者憑自己帳號登入登出
"""

# 登入


def login(request):
    """
    歡迎畫面
    ------------------------
    讓使用者憑自己帳號登入
    ------------------------
    DONE: 帳密錯誤提示訊息
    """
    shopAll = Shop.objects.all()
    if request.session.get('is_login', None):  # 不允許重複登入，已登入者轉跳/app/index
        return redirect('/app/index')

    if 'loginB' in request.POST:  # 已提交了帳號密碼，開始進行確認
        userId = request.POST['userId']
        userPw = request.POST['userPw']

        try:    # 偵測是否有選擇店鋪
            userShop = request.POST['loginShop']
        except:
            message = '請選擇店鋪'
            return render(request, 'login.html', locals())

        try:    # 先進資料庫比對帳號
            user = User.objects.get(user_id=userId)
        except:  # 帳號比對失敗
            message = '帳號不存在'
            return render(request, 'login.html', locals())

        if user.user_pw == userPw:  # 帳號比對成功，開始進行密碼比對
            # 密碼比對成功，開始將使用者資料放進session
            request.session['is_login'] = True
            request.session['user_id'] = user.user_id
            request.session['user_emp_id'] = user.user_emp_id
            request.session['cus_class_cus'] = 'default'

            irIdNow = ImportReport.objects.all().order_by('-ir_id')[0].ir_id
            request.session['irIdNow'] = irIdNow

            saleIdNow = Sale.objects.all().order_by('-sale_id')[0].sale_id
            request.session['saleIdNow'] = saleIdNow

            serv_id_now = Service.objects.all().order_by('-serv_id')[0].serv_id
            request.session['serv_id_now'] = serv_id_now

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

# 確認是否為登入狀態


def isLogin(request):
    if not request.session.get('is_login', None):  # 確認是否登入
        return False
    return True

# 登出


def logout(request):

    if not isLogin(request):  # 如果本來就沒登入
        return redirect('/app')

    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']

    return redirect('/app')

# 切換分店


def changeShop(request, a):
    request.session['user_shop'] = a
    request.session['user_shop_name'] = Shop.objects.get(shop_id=a).shop_name

    return redirect('/app/index')


"""
    主頁
    ------------------------
    視覺化報表呈現
    快速導覽
    ------------------------
    TODO: 待報表結算完成後，與其資料串接後呈現
"""

# 主頁


def index(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    """
    SMALLBOX
    """
    # 抓取庫存量
    try:
        stock_quantity = Stock.objects.count()
        numbers_of_member = Customer.objects.count()
        numbers_of_shop = Shop.objects.count()
    except:
        pass
    


    """
    CHATROOM
    """
    user_id_now = request.session['user_id']
    shop_id_now = request.session['user_shop']

    chat_messages = Message.objects.filter(
        group_name=shop_id_now).order_by("created")[:100]

    # 訊息
    message_list = []
    for message_item in chat_messages:
        employee = Employee.objects.get(emp_id=message_item.user.user_emp_id)
        emp_name_ch = employee.emp_name_ch

        message_list.append({
            'user': message_item.user,
            'emp_name_ch': emp_name_ch,
            'group_name': message_item.group_name,
            'message': message_item.message,
            'created': message_item.created
        })

    return render(request, 'index.html', locals())


"""
    人員管理
    ------------------------
    員工管理、顧客管理
"""
# 顧客管理
def nextCusId(prev_id):
    eng = prev_id[0:2]
    num = prev_id[2:7]
    num = int(num) + 1
    return eng + format(num, '05d')

def cus(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    persMenuOpen = "active menu-open"

    cusAll = Customer.objects.all().exclude(cus_seeable=False).exclude(cus_id='default')

    return render(request, 'cus.html', locals())

# 新增顧客
def addCus(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')

    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()
    prev_id = Customer.objects.all().exclude(cus_id='default').order_by('-cus_id')[0].cus_id
    next_id = nextCusId(prev_id)

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
    if not isLogin(request):    # 確認是否登入
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
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')

    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()
    
    if a == 'emp':
        persMenuOpen = "active menu-open"
        type = '員工'
        typeValue = a
        removedAll = Employee.objects.filter(emp_seeable=False)
        for removed in removedAll:
            removed.name = removed.emp_name_ch
            removed.id = removed.emp_id
    if a == 'cus':
        persMenuOpen = "active menu-open"
        type = '顧客'
        typeValue = a
        removedAll = Customer.objects.filter(cus_seeable=False)
        for removed in removedAll:
            removed.name = removed.cus_name
            removed.id = removed.cus_id
    if a == 'stock':
        stockMenuOpen = "active menu-open"
        type = '商品'
        typeValue = a
        removedAll = Stock.objects.filter(stock_seeable=False)
        for removed in removedAll:
            removed.name = removed.stock_name
            removed.id = removed.stock_id
    return render(request, 'removed.html', locals())


def restore(request, a, b):
    if a == 'emp':
        Employee.objects.filter(emp_id=b).update(emp_seeable=True)
        return redirect('/app/removed/emp')

    if a == 'cus':
        Customer.objects.filter(cus_id=b).update(cus_seeable=True)
        return redirect('/app/removed/cus')

    if a == 'stock':
        Stock.objects.filter(stock_id=b).update(stock_seeable=True)
        return redirect('/app/removed/stock')


def delete(request, a, b):
    if a == 'emp':
        Employee.objects.get(emp_id=b).delete()
        return redirect('/app/removed/emp')

    if a == 'cus':
        Customer.objects.get(cus_id=b).delete()
        return redirect('/app/removed/cus')

    if a == 'stock':
        return HttpResponse(a + "/" + b)
        # Customer.objects.get(stock_id=b).delete()
        # Instock.objects.filter(stock_id=b).delete()
        # return redirect('/app/removed/stock')
    if a == 'saleStock':
        sale_id = b[0:5]
        sale_stock_id = b[5:]
        Salestock.objects.get(
            salestock_sale = Sale.objects.get(sale_id = sale_id),
            salestock_stock = Stock.objects.get(stock_id = sale_stock_id)
        ).delete()
        return redirect('/app/sale')

    if a == 'saleAlloc':
        sale_id = b[0:5]
        sale_alloc_id = b[5:]
        Salealloc.objects.get(
            salealloc_sale = Sale.objects.get(sale_id = sale_id),
            salealloc_emp = Employee.objects.get(emp_id = sale_alloc_id)
        ).delete()
        return redirect('/app/sale')

def nextEmpId(prev_id):
    eng = prev_id[0:2]
    num = int(prev_id[2:5]) + 1
    return eng + format(num, '03d')

def emp(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')

    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    persMenuOpen = "active menu-open"

    empAll = Employee.objects.all().exclude(emp_seeable=False).exclude(emp_id='default')

    return render(request, 'emp.html', locals())


def addEmp(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')

    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()
    prev_id = Employee.objects.all().exclude(emp_id='default').order_by('-emp_id')[0].emp_id
    next_id = nextEmpId(prev_id)

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
    if not isLogin(request):    # 確認是否登入
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


"""
    前台交易
    ------------------------
    銷售與瀏覽紀錄
"""

# 銷售商品
def sale(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    userId = request.session['user_id']
    shopIdNow = request.session['user_shop']
    saleIdNow = request.session['saleIdNow']
    shopAll = Shop.objects.all()
    stockAll = Stock.objects.all().exclude(stock_seeable=False)
    for stock in stockAll:
        stock.instock_qua = Instock.objects.get(instock_id=stock.stock_id, instock_shop_id=shopIdNow).instock_qua
    cusAll = Customer.objects.all().exclude(cus_seeable=False).exclude(cus_id='default')
    empAll = Employee.objects.all().exclude(emp_seeable=False).exclude(emp_id='default')
    saleMenuOpen = "active menu-open"

    if Sale.objects.get(sale_id=saleIdNow).sale_complete:
        saleIdNext = nextSaleId(saleIdNow)
        saleIdNow = saleIdNext
        request.session['saleIdNow'] = saleIdNext
        Sale.objects.get_or_create(
            sale_id = saleIdNext,
            sale_cus = Customer.objects.get(cus_id='default'),
            sale_date = 'tmp',
            sale_person_in_charge = Employee.objects.get(emp_id='default'),
            sale_stock_price_total = 0,
            sale_price_total = 0,
            sale_point = 0,
            sale_pay = 'tmp',
            sale_type = 'tmp',
            sale_shop = Shop.objects.get(shop_id=shopIdNow),
            sale_remark = 'tmp',
            sale_created_by_user = User.objects.get(user_id = userId)
        )
    sale_now = Sale.objects.get(sale_id=saleIdNow)
    saleStockAll = sale_now.salestock_set.all()
    saleAllocAll = sale_now.salealloc_set.all()

    if 'nextB'in request.POST:
        for salestock in saleStockAll:
            Salestock.objects.filter(
                salestock_sale=sale_now,
                salestock_stock=salestock.salestock_stock
            ).update(
                salestock_price=request.POST[salestock.salestock_stock.stock_id + '_price'],
                salestock_amount=request.POST[salestock.salestock_stock.stock_id + '_amount'] 
            )
        for salealloc in saleAllocAll:
            Salealloc.objects.filter(
                salealloc_sale=sale_now,
                salealloc_emp=salealloc.salealloc_emp
            ).update(salealloc_perc=request.POST[salealloc.salealloc_emp.emp_id + '_perc'])

        return redirect('/app/sale/next')
    
    return render(request, 'sale.html', locals())

def nextSaleId(idNow):
    num = int(idNow[2:5])
    num += 1
    num = format(num, '03d')
    return 'ST' + str(num)

def saleNext(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    saleMenuOpen = "active menu-open"
    sale_id_now = request.session['saleIdNow']
    
    sale_now = Sale.objects.get(sale_id=sale_id_now)
    salestock_all = sale_now.salestock_set.all()

    stock_price_total = 0
    sale_price_total = 0
    sale_point_total = 0
    for salestock in salestock_all:
        sale_price_total += (salestock.salestock_price * salestock.salestock_amount)
        stock_price_total += (salestock.salestock_stock.stock_price * salestock.salestock_amount)
        if not salestock.salestock_stock.stock_point:
            sale_point_total = 0
        else:
            sale_point_total += (salestock.salestock_stock.stock_point * salestock.salestock_amount)

    if 'saveB' in request.POST:
        sale_date = request.POST['sale_date']
        sale_stock_price_total = request.POST['sale_stock_price_total']
        sale_price_total = request.POST['sale_price_total']
        sale_point = request.POST['sale_point']
        sale_pay = request.POST['sale_pay']
        sale_type = request.POST['sale_type']
        sale_remark = request.POST['sale_remark']

        Sale.objects.filter(sale_id=sale_id_now).update(
            sale_date = sale_date,
            sale_stock_price_total = sale_stock_price_total,
            sale_price_total = sale_price_total,
            sale_point = sale_point,
            sale_pay = sale_pay,
            sale_type = sale_type,
            sale_remark = sale_remark,
            sale_complete = True
        )

        for salestock in salestock_all:
            if salestock.salestock_stock.stock_type == '儲值卡':
                CustomerClass.objects.create(
                    cuscl_cus = sale_now.sale_cus,
                    cuscl_stock = salestock.salestock_stock,
                    cuscl_quantity = 12
                )

        return redirect('/app/sale')




    return render(request, 'saleNext.html', locals())

def selectSale(request, a, b):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    sale_id = a
    select_stock = b
    sale_now = Sale.objects.get(sale_id=sale_id)
    sale_now.salestock_set.get_or_create(
        salestock_stock = Stock.objects.get(stock_id=select_stock),
        salestock_price = 0,
        salestock_amount = 0
    )

    return redirect('/app/sale')

def servIdNext(id_now):
    num = int(id_now[2:5])
    num += 1
    num = format(num, '03d')
    return 'SV' + str(num)

# 課程扣點
def service(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    user_id_now = request.session['user_id']
    shopNow = request.session['user_shop_name']
    shop_id_now = request.session['user_shop']
    serv_id_now = request.session['serv_id_now']
    shopAll = Shop.objects.all()
    serviceAll = Stock.objects.filter(stock_type='服務')
    empAll = Employee.objects.all().exclude(emp_seeable = False).exclude(emp_id='default')
    cusAll = Customer.objects.all().exclude(cus_seeable = False).exclude(cus_id='default')
    saleMenuOpen = "active menu-open"

    if Service.objects.get(serv_id=serv_id_now).serv_complete:
        serv_id_next = servIdNext(serv_id_now)
        serv_id_now = serv_id_next
        request.session['serv_id_now'] = serv_id_next
        Service.objects.get_or_create(
            serv_id = serv_id_next,
            serv_cus = Customer.objects.get(cus_id='default'),
            serv_date = 'tmp',
            serv_stock = Stock.objects.get(stock_id='default'),
            serv_emp1 = Employee.objects.get(emp_id='default'),
            serv_emp2 = Employee.objects.get(emp_id='default'),
            serv_emp3 = Employee.objects.get(emp_id='default'),
            serv_stock_price = 0,
            serv_price = 0,
            serv_point = 0,
            serv_pay = 'tmp',
            serv_type = 'tmp',
            serv_shop = Shop.objects.get(shop_id=shop_id_now),
            serv_remark = 'tmp',
            serv_created_by_user = User.objects.get(user_id = user_id_now)
        )
    serv_now = Service.objects.get(serv_id=serv_id_now)

    
    return render(request, 'service.html', locals())

def selectService(request, a, b):
    service_id = a
    select_service = b

    Service.objects.filter(serv_id=service_id).update(
        serv_stock=Stock.objects.get(stock_id=select_service)
    )

    return redirect('/app/service')

def servNext(request, a):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    serv_now = Service.objects.get(serv_id=a)
    serv_stock_price = serv_now.serv_stock.stock_price
    serv_point = serv_now.serv_stock.stock_point
    serv_price = serv_now.serv_stock.stock_price
    if serv_now.serv_stock.stock_type == '儲值卡':
        serv_stock_price = int(serv_now.serv_stock.stock_price / 10)
        serv_price = int(serv_stock_price)
        serv_point = int(serv_price / 10)
    if 'saveB' in request.POST:
        serv_date = request.POST['serv_date']
        serv_stock_price = request.POST['serv_stock_price']
        serv_price = request.POST['serv_price']
        serv_point = serv_now.serv_stock.stock_point
        serv_pay = request.POST['serv_pay']
        serv_type = request.POST['serv_type']
        serv_remark = request.POST['serv_remark']

        Service.objects.filter(serv_id=a).update(
            serv_date = serv_date,
            serv_stock_price = serv_stock_price,
            serv_price = serv_price,
            serv_point = serv_point,
            serv_pay = serv_pay,
            serv_type = serv_type,
            serv_remark = serv_remark,
            serv_complete = True
        )

        return redirect('/app/service')

    return render(request, 'servNext.html', locals())

def deduct(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()
    cus_all = Customer.objects.all().exclude(cus_seeable=False)
    saleMenuOpen = "active menu-open"
    cus_class_cus = request.session['cus_class_cus']
    if cus_class_cus == '此客戶無擁有課程':
        cus_class_all = cus_class_cus
    else:
        cus_class_all = CustomerClass.objects.filter(
            cuscl_cus=Customer.objects.get(cus_id=cus_class_cus)
        )

    

    return render(request, 'deduct.html', locals())

def deductService(request, a):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    serv_id_now = request.session['serv_id_now']
    user_id_now = request.session['user_id']
    shop_id_now = request.session['user_shop']
    cus_class_cus = request.session['cus_class_cus']
    cuscl_stock_now = Stock.objects.get(stock_id=a)
    
    cuscl_qua = CustomerClass.objects.get(cuscl_cus=Customer.objects.get(cus_id=cus_class_cus)).cuscl_quantity - 1
    CustomerClass.objects.filter(cuscl_cus=Customer.objects.get(cus_id=cus_class_cus)).update(cuscl_quantity=cuscl_qua)

    if Service.objects.get(serv_id=serv_id_now).serv_complete:
        serv_id_next = servIdNext(serv_id_now)
        serv_id_now = serv_id_next
        request.session['serv_id_now'] = serv_id_next
        Service.objects.create(
            serv_id = serv_id_next,
            serv_cus = Customer.objects.get(cus_id=cus_class_cus),
            serv_date = 'tmp',
            serv_stock = cuscl_stock_now,
            serv_emp1 = Employee.objects.get(emp_id='default'),
            serv_emp2 = Employee.objects.get(emp_id='default'),
            serv_emp3 = Employee.objects.get(emp_id='default'),
            serv_stock_price = 0,
            serv_price = 0,
            serv_point = 0,
            serv_pay = 'tmp',
            serv_type = 'tmp',
            serv_shop = Shop.objects.get(shop_id=shop_id_now),
            serv_remark = 'tmp',
            serv_created_by_user = User.objects.get(user_id = user_id_now)
        )
    Service.objects.filter(serv_id=serv_id_now).update(
        serv_cus = Customer.objects.get(cus_id=cus_class_cus),
        serv_stock = cuscl_stock_now,
    )

    return redirect('/app/service')

# 交易紀錄
def saleLog(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()
    reportMenuOpen = "active menu-open"

    if 'searchB' in request.POST:
        select_section = request.POST['selectSection']
        serv_all = Service.objects.all().exclude(serv_id='SV000').exclude(serv_complete=False)
        sale_all = Sale.objects.all().exclude(sale_id='ST000').exclude(sale_complete=False)
        for sale in sale_all:
            sale.st_all = sale.salestock_set.all()
            sale.sa_all = sale.salealloc_set.all()

    return render(request, 'report.html', locals())

# 選擇人員
def selectPerson(request, a, b, c):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')

    select_type = a
    select_sale_id = b
    select_person_id = c

    if select_type == 'cus':
        Sale.objects.filter(sale_id=select_sale_id).update(sale_cus=Customer.objects.get(cus_id=select_person_id))
        return redirect('/app/sale')
    if select_type == 'emp':
        Sale.objects.filter(sale_id=select_sale_id).update(sale_person_in_charge=Employee.objects.get(emp_id=select_person_id))
        return redirect('/app/sale')
    if select_type == 'empAlloc':
        sale_now = Sale.objects.get(sale_id=select_sale_id)
        sale_now.salealloc_set.get_or_create(
            salealloc_emp = Employee.objects.get(emp_id=select_person_id),
            salealloc_perc = 0
        )
        return redirect('/app/sale')
    if select_type == 'serv_cus':
        Service.objects.filter(serv_id=select_sale_id).update(
            serv_cus=Customer.objects.get(cus_id=select_person_id)
        )
        return redirect('/app/service')
    if select_type == 'serv_emp1':
        Service.objects.filter(serv_id=select_sale_id).update(
            serv_emp1=Employee.objects.get(emp_id=select_person_id)
        )
        return redirect('/app/service')
    if select_type == 'serv_emp2':
        Service.objects.filter(serv_id=select_sale_id).update(
            serv_emp2=Employee.objects.get(emp_id=select_person_id)
        )
        return redirect('/app/service')
    if select_type == 'serv_emp3':
        Service.objects.filter(serv_id=select_sale_id).update(
            serv_emp3=Employee.objects.get(emp_id=select_person_id)
        )
        return redirect('/app/service')
    if select_type == 'deduct_cus':
        if not CustomerClass.objects.filter(
            cuscl_cus=Customer.objects.get(cus_id=select_person_id)
        ):
            cus_class_cus = '此客戶無擁有課程'
        else:
            cus_class_cus = select_person_id

        request.session['cus_class_cus'] = cus_class_cus
        return redirect('/app/deduct/')
        
    
            

"""
    庫存管理
    ------------------------
    品項管理、進出貨
"""
def stock(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    stockMenuOpen = "active menu-open"

    stockAll = Stock.objects.all().exclude(stock_seeable=False).exclude(stock_id='default')

    # 庫存量目前有空值，待修改
    for stock in stockAll:
        try:
            stock.instock_qua = Instock.objects.get(
                instock_id=stock.stock_id, instock_shop_id=request.session['user_shop']
            ).instock_qua
        except:
            stock.instock_qua = 10

    return render(request, 'stock.html', locals())

def addStock(request):
    if not isLogin(request):    # 確認是否登入
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
            Instock.objects.create(
                instock_id=stock_id, instock_shop_id=shop.shop_id, instock_qua=0, instock_salesvolume=0)

        return redirect('/app/stock')

    return render(request, 'addStock.html', locals())


def editStock(request, row_index):
    
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')

    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    stockMenuOpen = "active menu-open"

    stockThis = Stock.objects.get(stock_id=row_index)

    if 'saveB' in request.POST:  # 提交新數據
        stock_type = request.POST['stock_type']
        stock_id = request.POST['stock_id']
        stock_name = request.POST['stock_name']
        stock_price = request.POST['stock_price']
        stock_cost = request.POST['stock_cost']
        stock_point = request.POST['stock_point']
        stock_remark = request.POST['stock_remark']

        Stock.objects.filter(stock_id=row_index).update(stock_type=stock_type, stock_id=stock_id, stock_name=stock_name,
                             stock_price=stock_price, stock_cost=stock_cost, stock_point=stock_point, stock_remark=stock_remark)
        
        return redirect('/app/stock')

    if 'removeB' in request.POST:
        Stock.objects.filter(stock_id=row_index).update(stock_seeable=False)
        
        return redirect('/app/stock')

    return render(request, 'editStock.html', locals())
    
    # return HttpResponse("待完善")

def exportStock(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    stockMenuOpen = "active menu-open"
    return render(request, 'exportStock.html', locals())


def nextIrId(idNow):
    num = int(idNow[2:5])
    num += 1
    num = format(num, '03d')
    return 'IM' + str(num)


def importStock(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopIdNow = request.session['user_shop']
    shopAll = Shop.objects.all()

    stockMenuOpen = "active menu-open"

    stockAll = Stock.objects.all()
    for stock in stockAll:
        stock.instock_qua = Instock.objects.get(
            instock_id=stock.stock_id, instock_shop_id=request.session['user_shop']).instock_qua

    irIdNow = request.session['irIdNow']

    if ImportReport.objects.get(ir_id=irIdNow).ir_complete:
        irIdNext = nextIrId(irIdNow)
        irIdNow = irIdNext
        request.session['irIdNow'] = irIdNext
        ImportReport.objects.create(
            ir_id=irIdNext, ir_date='tmp', ir_complete=False)
    selectedStockAll = ImportStock.objects.filter(is_ir_id=irIdNow)
    for selectedStock in selectedStockAll:
        selectedStock.stock_name = Stock.objects.get(
            stock_id=selectedStock.is_stock_id).stock_name

    if 'saveB' in request.POST:
        ir_date = request.POST['ir_date']
        ir_remark = request.POST['ir_remark']
        ir_complete = True

        for stock in selectedStockAll:
            is_from_shop_id = request.POST[stock.is_stock_id +
                                           '_is_from_shop_id']
            is_qua = request.POST[stock.is_stock_id + '_is_qua']

            stockQuaNow = Instock.objects.get(
                instock_id=stock.is_stock_id, instock_shop_id=shopIdNow).instock_qua
            Instock.objects.filter(instock_id=stock.is_stock_id, instock_shop_id=shopIdNow).update(
                instock_qua=stockQuaNow+int(is_qua))

            if not is_from_shop_id == 'out':
                fromStockQuaNow = Instock.objects.get(
                    instock_id=stock.is_stock_id, instock_shop_id=is_from_shop_id).instock_qua
                Instock.objects.filter(instock_id=stock.is_stock_id, instock_shop_id=is_from_shop_id).update(
                    instock_qua=fromStockQuaNow-int(is_qua))

            ImportStock.objects.filter(is_ir_id=request.session['irIdNow']).update(
                is_from_shop_id=is_from_shop_id, is_qua=is_qua)

        ImportReport.objects.filter(ir_id=request.session['irIdNow']).update(
            ir_date=ir_date, ir_remark=ir_remark, ir_complete=ir_complete)

        return redirect('/app/stock')

    return render(request, 'importStock.html', locals())


def selectImport(request, a, b):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')

    irIdNow = a
    selectStock = b
    ImportStock.objects.create(
        is_ir_id=irIdNow, is_stock_id=selectStock, is_qua=0, is_from_shop_id='')

    return redirect('/app/importStock/')


"""
    報表結算
    ------------------------
    結算選定時間內的資料
"""
# 庫存清算
def stockReport(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    reportMenuOpen = "active menu-open"
    return render(request, 'stockReport.html', locals())

# 薪資獎金計算
def salaryCount(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()
    emp_all = Employee.objects.all().exclude(emp_id='default')
    SSE_all = SalarySelectEmp.objects.all()

    reportMenuOpen = "active menu-open"
    return render(request, 'salaryCount.html', locals())

def salaryCountNext(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    emp_all = SalarySelectEmp.objects.all()
    SalaryResult.objects.all().delete()

    for emp in emp_all:
        stock_income_all = 0
        stock_point_all = 0
        head_income_all_emp1 = 0
        head_income_all_emp2 = 0
        head_income_all_emp3 = 0
        head_point_all_emp1 = 0
        head_point_all_emp2 = 0
        head_point_all_emp3 = 0
        hair_income_all_emp1 = 0
        hair_income_all_emp2 = 0
        hair_income_all_emp3 = 0
        hair_point_all_emp1 = 0
        hair_point_all_emp2 = 0
        hair_point_all_emp3 = 0
        
        sale_all = Sale.objects.all().exclude(sale_complete=False).exclude(sale_id='ST000')
        for sale in sale_all:
            sale_alloc_all = sale.salealloc_set.all()
            for sale_alloc in sale_alloc_all:
                if sale_alloc.salealloc_emp == emp.SSE_emp:
                    perc = sale_alloc.salealloc_perc
                    stock_point_all += sale.sale_point * perc / 100                   #商品銷售總計積
                    stock_income_all += sale.sale_price_total * perc / 100            #商品銷售總收入
        
        serv_all = Service.objects.all().exclude(serv_complete=False).exclude(serv_id='SV000')
        for serv in serv_all:
            if serv.serv_type == 'income_head':
                if serv.serv_emp1 == emp.SSE_emp:  
                    MSP_all = MultiSevicePercent.objects.all()
                    for MSP in MSP_all:
                        if serv.serv_stock.stock_name == MSP.MSP_name:
                            head_income_all_emp1 += serv.serv_price * MSP.MSP_emp1 / 100     #頭皮護理專業操作總收入
                            head_point_all_emp1 += serv.serv_point * MSP.MSP_emp1 / 100      #頭皮護理專業操作總計積
                if serv.serv_emp2 == emp.SSE_emp:
                    MSP_all = MultiSevicePercent.objects.all()
                    for MSP in MSP_all:
                        if serv.serv_stock.stock_name == MSP.MSP_name:
                            head_income_all_emp2 += serv.serv_price * MSP.MSP_emp2 / 100     #頭皮護理洗髮總收入
                            head_point_all_emp2 += serv.serv_point * MSP.MSP_emp2 / 100      #頭皮護理洗髮總計機
                if serv.serv_emp3 == emp.SSE_emp:
                    MSP_all = MultiSevicePercent.objects.all()
                    for MSP in MSP_all:
                        if serv.serv_stock.stock_name == MSP.MSP_name:
                            head_income_all_emp3 += serv.serv_price * MSP.MSP_emp3 / 100     #頭皮護理吹整造型總收入
                            head_point_all_emp3 += serv.serv_point * MSP.MSP_emp3 / 100      #頭皮護理吹整造型總總計積
            if serv.serv_type == 'income_hair':
                if serv.serv_emp1 == emp.SSE_emp:
                    MSP_all = MultiSevicePercent.objects.all()
                    for MSP in MSP_all:
                        if serv.serv_stock.stock_name == MSP.MSP_name:
                            hair_income_all_emp1 += serv.serv_price * MSP.MSP_emp1 / 100     #洗剪染燙專業操作總收入
                            hair_point_all_emp1 += serv.serv_point * MSP.MSP_emp1 / 100      #洗剪染燙專業操作總計積
                if serv.serv_emp2 == emp.SSE_emp:
                    MSP_all = MultiSevicePercent.objects.all()
                    for MSP in MSP_all:
                        if serv.serv_stock.stock_name == MSP.MSP_name:
                            hair_income_all_emp2 += serv.serv_price * MSP.MSP_emp2 / 100     #洗剪染燙洗髮總收入
                            hair_point_all_emp2 += serv.serv_point * MSP.MSP_emp2 / 100      #洗剪染燙洗髮總計機
                if serv.serv_emp3 == emp.SSE_emp:
                    MSP_all = MultiSevicePercent.objects.all()
                    for MSP in MSP_all:
                        if serv.serv_stock.stock_name == MSP.MSP_name:
                            hair_income_all_emp3 += serv.serv_price * MSP.MSP_emp3 / 100     #洗剪染燙吹整造型總收入
                            hair_point_all_emp3 += serv.serv_point * MSP.MSP_emp3 / 100      #洗剪染燙吹整造型總總計積

        head_income_all = head_income_all_emp1 + head_income_all_emp2 + head_income_all_emp3  #頭皮護理總收入
        hair_income_all = hair_income_all_emp1 + hair_income_all_emp2 + hair_income_all_emp3  #洗剪染燙總收入

        comm_all  = Commission.objects.all()
        for comm in comm_all:
            CIT_all = comm.commincometype_set.all()
            for CIT in CIT_all:
                if CIT.CIT_type == '頭皮護理收入':
                    CL_all = comm.commlimit_set.all()
                    for CL in CL_all:
                        if head_income_all >= CL.CL_income_limit:
                            percent_now = CL.CL_bonus_perc
                        elif head_income_all < CL.CL_income_limit:
                            break
                    head_income_all_comm = head_income_all * percent_now / 100    #頭皮護理收入提成結果
                if CIT.CIT_type == '洗剪染燙收入':
                    CL_all = comm.commlimit_set.all()
                    for CL in CL_all:
                        if hair_income_all >= CL.CL_income_limit:
                            percent_now = CL.CL_bonus_perc
                        elif hair_income_all < CL.CL_income_limit:
                            break
                    hair_income_all_comm = hair_income_all * percent_now / 100    #洗剪染燙收入提成結果
                else:
                    CL_all = comm.commlimit_set.all()
                    for CL in CL_all:
                        if stock_income_all >= CL.CL_income_limit:
                            percent_now = CL.CL_bonus_perc
                        elif stock_income_all < CL.CL_income_limit:
                            break
                    stock_income_all_comm = stock_income_all * percent_now / 100    #商品收入提成結果

        SR_result = emp.SSE_emp.emp_salary + head_income_all_comm + hair_income_all_comm + stock_income_all_comm + stock_point_all + head_point_all_emp1 + head_point_all_emp2 + head_point_all_emp3 + hair_point_all_emp1 + hair_point_all_emp2 + hair_point_all_emp3
        
        SalaryResult.objects.create(
            SR_emp = emp.SSE_emp,
            stock_point_all = int(stock_point_all + 0.5),
            stock_income_all = int(stock_income_all + 0.5),
            head_income_all_emp1 = int(head_income_all_emp1 + 0.5),
            head_point_all_emp1 = int(head_point_all_emp1 + 0.5),
            head_income_all_emp2 = int(head_income_all_emp2 + 0.5),
            head_point_all_emp2 = int(head_point_all_emp2 + 0.5),
            head_income_all_emp3 = int(head_income_all_emp3 + 0.5),
            head_point_all_emp3 = int(head_point_all_emp3 + 0.5),
            hair_income_all_emp1 = int(hair_income_all_emp1 + 0.5),
            hair_point_all_emp1 = int(hair_point_all_emp1 + 0.5),
            hair_income_all_emp2 = int(hair_income_all_emp2 + 0.5),
            hair_point_all_emp2 = int(hair_point_all_emp2 + 0.5),
            hair_income_all_emp3 = int(hair_income_all_emp3 + 0.5),
            hair_point_all_emp3 = int(hair_point_all_emp3 + 0.5),
            head_income_all = int(head_income_all + 0.5),
            hair_income_all = int(hair_income_all + 0.5),
            head_income_all_comm = int(head_income_all_comm + 0.5),
            hair_income_all_comm = int(hair_income_all_comm + 0.5),
            stock_income_all_comm = int(stock_income_all_comm + 0.5),
            SR_result = int(SR_result + 0.5)
        )
    SR_all = SalaryResult.objects.all()
    for SR in SR_all:
        SR.salary = SR.SR_emp.emp_salary 

    SalarySelectEmp.objects.all().delete()

    return render(request, 'salaryCountNext.html', locals())

def selectSalaryEmp(reques, a):
    SalarySelectEmp.objects.create(
        SSE_emp = Employee.objects.get(emp_id=a)
        )
    return redirect('/app/salaryCount')

# 營業額計算
def turnoverCount(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    reportMenuOpen = "active menu-open"
    return render(request, 'turnoverCount.html', locals())

"""
    系統設定
    ------------------------
    牽涉系統全域的設定
    ------------------------
    TODO: 店鋪管理介面待完成
"""
def setting(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    return render(request, 'setting.html', locals())


def setShop(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    return render(request, 'setShop.html', locals())


def addShop(request):
    if not isLogin(request):    # 確認是否登入
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
            Instock.objects.create(
                instock_id=stock.stock_id, instock_shop_id=shop_id, instock_qua=0, instock_salesvolume=0)

        return redirect('/app/setting/shop')

    return render(request, 'addShop.html', locals())

def nextSalaryCode(code_prev):
    if code_prev[0:3] == "MSP":
        eng = code_prev[0:3]
        num = int(code_prev[3:6]) + 1
        return eng + format(num, '03d')
    eng = code_prev[0:2]
    num = int(code_prev[2:5]) + 1
    return eng + format(num, '03d')

def setSalary(request):
    salary_all = []
    RB_all = RegularBonus.objects.all()
    CM_all = Commission.objects.all().exclude(comm_code='tmp')
    MSP_all = MultiSevicePercent.objects.all()
    for RB in RB_all:
        tmp = {'name' : RB.bonus_name}
        salary_all.append(tmp)
    for CM in CM_all:
        tmp = {'name' : CM.comm_name}
        salary_all.append(tmp)
    for MSP in MSP_all:
        tmp = {'name' : MSP.MSP_name}
        salary_all.append(tmp)
    return render(request, 'setSalary.html', locals())

def addSalary(request):
    return render(request, 'addSalary.html', locals())


def addSalaryA(request, a):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()
    if a == 'comm':
        cit_all = CommIncomeType.objects.filter(
            CIT_comm = Commission.objects.get(comm_code = 'tmp')
        )
        cl_all = CommLimit.objects.filter(
            CL_comm = Commission.objects.get(comm_code = 'tmp')
        )

        code_prev = Commission.objects.all().exclude(comm_code = 'tmp').order_by('-comm_code')[0].comm_code
        code_now = nextSalaryCode(code_prev)

        if 'addB' in request.POST:
            limit = request.POST['limit']
            perc = request.POST['perc']
            CommLimit.objects.create(
                CL_comm = Commission.objects.get(comm_code = 'tmp'),
                CL_income_limit = limit,
                CL_bonus_perc = perc
            )
            return redirect('/app/setting/addSalary/comm')
        
        if 'saveB' in request.POST:
            name = request.POST['name']
            code = request.POST['code']
            Commission.objects.create(
                comm_name = name,
                comm_code = code
            )
            CommIncomeType.objects.filter(
                CIT_comm = Commission.objects.get(comm_code = 'tmp')
            ).update(
                CIT_comm = Commission.objects.get(comm_code = code)
            )

            CommLimit.objects.filter(
                CL_comm = Commission.objects.get(comm_code = 'tmp')
            ).update(
                CL_comm = Commission.objects.get(comm_code = code)
            )
            return redirect('/app/setting/salary')
    
        return render(request, 'addSalaryComm.html', locals())

    if a == 'regularBonus':
        code_prev = RegularBonus.objects.all().order_by('-bonus_code')[0].bonus_code
        code_now = nextSalaryCode(code_prev)
        if 'saveB' in request.POST:
            name = request.POST['name']
            value = request.POST['value']
            code = request.POST['code']
            RegularBonus.objects.create(
                bonus_name = name,
                bonus_code = code,
                bonus_value = value
            )
            return redirect('/app/setting/salary')

        return render(request, 'addSalaryRegular.html', locals())

    if a == 'MSP':
        code_prev = MultiSevicePercent.objects.all().order_by('-MSP_code')[0].MSP_code
        code_now = nextSalaryCode(code_prev)
        if 'saveB' in request.POST:
            name = request.POST['name']
            code = request.POST['code']
            emp1 = request.POST['emp1']
            emp2 = request.POST['emp2']
            emp3 = request.POST['emp3']
            MultiSevicePercent.objects.create(
                    MSP_name = name,
                    MSP_code = code,
                    MSP_emp1 = emp1,
                    MSP_emp2 = emp2,
                    MSP_emp3 = emp3
            )
            return redirect('/app/setting/salary')
        return render(request, 'addSalaryMSP.html', locals())
def addCIT(request, a):
    CommIncomeType.objects.create(
        CIT_comm = Commission.objects.get(comm_code='tmp'),
        CIT_type = a
    )
    return redirect('/app/setting/addSalary/comm')



"""
    員工福利區
    ------------------------
    牽涉系統全域的設定
    ------------------------
    TODO: 店鋪管理介面待完成
"""
def ok(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()
    return render(request, 'ok.html', locals())
