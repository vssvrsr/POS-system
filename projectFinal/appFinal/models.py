from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=50, unique=True)
    user_pw = models.CharField(max_length=50)
    user_emp_id = models.CharField(max_length=50)

    def __str__(self):
        return self.user_id


class LogedIn(models.Model):
    loged_user = models.CharField(max_length=50)
    loged_ip = models.CharField(max_length=50)

    def __str__(self):
        return self.loged_ip


class Customer(models.Model):
    # cus_photo = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    cus_name = models.CharField(max_length=50)
    cus_name_en = models.CharField(max_length=50, null=True)
    cus_id = models.CharField(max_length=50, unique=True)
    cus_idcard = models.CharField(max_length=50, null=True)
    cus_class = models.CharField(max_length=50, null=True)
    cus_sex = models.CharField(max_length=50, null=True)
    cus_phone1 = models.CharField(max_length=50)
    cus_phone2 = models.CharField(max_length=50, null=True)
    cus_addr1 = models.CharField(max_length=50, null=True)
    cus_addr2 = models.CharField(max_length=50, null=True)
    cus_email = models.CharField(max_length=50, null=True)
    cus_bd = models.CharField(max_length=50, null=True)
    cus_shop_id = models.CharField(max_length=50, null=True)
    cus_arr_date = models.CharField(max_length=50)

    cus_seeable = models.BooleanField(default=True)

    cus_source = models.CharField(max_length=50, null=True)
    cus_remark = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.cus_name


class Employee(models.Model):
    # emp_photo = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    emp_id = models.CharField(max_length=50, unique=True)
    # emp_cus_id =
    emp_name_ch = models.CharField(max_length=50)
    emp_name_en = models.CharField(max_length=50, null=True)
    emp_idcard = models.CharField(max_length=50, null=True)
    emp_class = models.CharField(max_length=50)
    emp_salary = models.IntegerField()
    emp_bd = models.CharField(max_length=50)
    emp_arr_date = models.CharField(max_length=50)
    emp_leave_date = models.CharField(max_length=50)
    emp_shop_id = models.CharField(max_length=50)
    # emp_limit

    emp_phone1 = models.CharField(max_length=50)
    emp_phone2 = models.CharField(max_length=50, null=True)
    emp_addr1 = models.CharField(max_length=50, null=True)
    emp_addr2 = models.CharField(max_length=50, null=True)
    emp_email = models.EmailField(max_length=254, null=True)

    # emp_system_login
    emp_seeable = models.BooleanField(default=True)

    emp_remark = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.emp_name_ch


class Shop(models.Model):
    shop_id = models.CharField(max_length=50, unique=True)
    shop_name = models.CharField(max_length=50)
    shop_class = models.CharField(max_length=50)
    shop_addr = models.CharField(max_length=50)
    shop_phone1 = models.CharField(max_length=50)
    shop_phone2 = models.CharField(max_length=50, null=True)
    shop_remark = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.shop_name

# 庫存管理


class Stock(models.Model):
    stock_type = models.CharField(max_length=50)
    stock_id = models.CharField(max_length=50, unique=True)
    stock_name = models.CharField(max_length=50)
    stock_price = models.IntegerField()
    stock_cost = models.IntegerField(null=True)
    stock_point = models.IntegerField(null=True)
    stock_seeable = models.BooleanField(default=True)
    stock_remark = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.stock_name


class Instock(models.Model):
    instock_id = models.CharField(max_length=50)
    instock_shop_id = models.CharField(max_length=50)
    instock_qua = models.IntegerField(default=0)
    instock_salesvolume = models.IntegerField(default=0)

    def __str__(self):
        return self.instock_id


class ImportReport(models.Model):
    ir_id = models.CharField(max_length=50)
    ir_date = models.CharField(max_length=50)
    ir_remark = models.CharField(max_length=300, null=True)
    ir_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.ir_id


class ImportStock(models.Model):
    is_ir_id = models.CharField(max_length=50)
    is_stock_id = models.CharField(max_length=50)
    is_qua = models.IntegerField()
    is_from_shop_id = models.CharField(max_length=50)

    def __str__(self):
        return self.is_ir_id

class Sale(models.Model):
    sale_id = models.CharField(max_length=50)
    sale_cus = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sale_date = models.CharField(max_length=50)
    sale_person_in_charge = models.ForeignKey(Employee, on_delete=models.CASCADE)
    sale_stock_price_total = models.IntegerField()
    sale_price_total = models.IntegerField()
    sale_point = models.IntegerField()
    sale_pay = models.CharField(max_length=50)
    sale_type = models.CharField(max_length=50)
    sale_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    sale_remark = models.CharField(max_length=50)
    sale_created_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='create_by_this_user', null=True)
    sale_modified_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_by_this_user', null=True)
    sale_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.sale_id

class Salestock(models.Model):
    salestock_sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    salestock_stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    salestock_price = models.IntegerField()
    salestock_amount = models.IntegerField()

    def __str__(self):
        return self.salestock_sale.sale_id

class Salealloc(models.Model):
    salealloc_sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    salealloc_emp = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salealloc_perc = models.IntegerField()

    def __str__(self):
        return self.salealloc_sale.sale_id

class Service(models.Model):
    serv_id = models.CharField(max_length=50)
    serv_cus = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # serv_person_in_charge = models.ForeignKey(Employee, on_delete=models.CASCADE)
    serv_date = models.CharField(max_length=50)

    serv_stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    serv_emp1 = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='serv_by_emp1')
    serv_emp2 = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='serv_by_emp2')
    serv_emp3 = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='serv_by_emp3')

    serv_stock_price = models.IntegerField()
    serv_price = models.IntegerField()
    serv_point = models.IntegerField()
    serv_pay = models.CharField(max_length=50)
    serv_type = models.CharField(max_length=50)
    serv_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)

    serv_remark = models.CharField(max_length=50)

    serv_created_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='create_by_this_user_serv')
    serv_modified_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_by_this_user_serv', null=True)

    serv_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.serv_id

class CustomerClass(models.Model):
    cuscl_cus = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cuscl_stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    cuscl_quantity = models.IntegerField()

    def __str__(self):
        return self.cuscl_cus.cus_id