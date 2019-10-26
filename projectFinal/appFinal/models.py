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