from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import User, Customer, LogedIn, Employee, Shop, Stock, Instock, ImportReport, ImportStock, Sale, Salestock, Salealloc


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

            irIdNow = ImportReport.objects.all().order_by('-ir_id')[0].ir_id
            request.session['irIdNow'] = irIdNow

            saleIdNow = Sale.objects.all().order_by('-sale_id')[0].sale_id
            request.session['saleIdNow'] = saleIdNow

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

    return render(request, 'index.html', locals())


"""
    人員管理
    ------------------------
    員工管理、顧客管理
"""
# 
def cus(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    persMenuOpen = "active menu-open"

    cusAll = Customer.objects.all().exclude(cus_seeable=False)

    return render(request, 'cus.html', locals())


def addCus(request):
    if not isLogin(request):    # 確認是否登入
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
        return redirect('/app/removed/stock')

    if a == 'stock':
        Customer.objects.get(stock_id=b).delete()
        Instock.objects.filter(stock_id=b).delete()
        return redirect('/app/removed/cus')


def emp(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')

    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    persMenuOpen = "active menu-open"

    empAll = Employee.objects.all().exclude(emp_seeable=False)

    return render(request, 'emp.html', locals())


def addEmp(request):
    if not isLogin(request):    # 確認是否登入
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
    cusAll = Customer.objects.all().exclude(cus_seeable=False)
    empAll = Employee.objects.all().exclude(emp_seeable=False)
    saleMenuOpen = "active menu-open"

    if Sale.objects.get(sale_id=saleIdNow).sale_complete:
        saleIdNext = nextSaleId(saleIdNow)
        saleIdNow = saleIdNext
        request.session['saleIdNow'] = saleIdNext
        Sale.objects.create(
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

        return redirect('/app/sale')




    return render(request, 'saleNext.html', locals())

def selectSale(request, a, b):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    sale_id = a
    select_stock = b
    sale_now = Sale.objects.get(sale_id=sale_id)
    sale_now.salestock_set.create(
        salestock_stock = Stock.objects.get(stock_id=select_stock),
        salestock_price = 0,
        salestock_amount = 0
    )

    return redirect('/app/sale')

# 課程扣點
def service(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()
    serviceAll = Stock.objects.filter(stock_type='服務')
    empAll = Employee.objects.all().exclude(emp_seeable = False)
    cusAll = Customer.objects.all().exclude(cus_seeable = False)

    saleMenuOpen = "active menu-open"
    return render(request, 'service.html', locals())

# 交易紀錄
def saleLog(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    saleMenuOpen = "active menu-open"
    return render(request, 'report.html', locals())

# TODO: 補上comment
def selectPerson(request, a, b, c):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')

    select_type = a
    select_sale_id = b
    select_person_id = c

    if select_type == 'cus':
        Sale.objects.filter(sale_id=select_sale_id).update(sale_cus=Customer.objects.get(cus_id=select_person_id))
    if select_type == 'emp':
        Sale.objects.filter(sale_id=select_sale_id).update(sale_person_in_charge=Employee.objects.get(emp_id=select_person_id))
    if select_type == 'empAlloc':
        sale_now = Sale.objects.get(sale_id=select_sale_id)
        sale_now.salealloc_set.create(
            salealloc_emp = Employee.objects.get(emp_id=select_person_id),
            salealloc_perc = 0
        )
        

    return redirect('/app/sale')

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

    stockAll = Stock.objects.all().exclude(stock_seeable=False)

    # 庫存量目前有空值，待修改
    for stock in stockAll:
        try:
            stock.instock_qua = Instock.objects.get(
            instock_id=stock.stock_id, instock_shop_id=request.session['user_shop']).instock_qua
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
    
    ### return HttpResponse("待完善")


def deduct(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    saleMenuOpen = "active menu-open"
    return render(request, 'deduct.html', locals())


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
    return HttpResponse("庫存清算:待完成")

# 薪資獎金計算
def salaryCount(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')
    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    reportMenuOpen = "active menu-open"
    return render(request, 'salaryCount.html', locals())

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

