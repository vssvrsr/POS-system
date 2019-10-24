from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=50, unique=True)
    user_pw = models.CharField(max_length=50)
    user_emp_id = models.CharField(max_length=50)

    def __str__(self):
        return self.user_id

class Customer(models.Model):
    # cus_photo = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    cus_name = models.CharField(max_length=50)
    cus_name_en = models.CharField(max_length=50, null=True)
    cus_id = models.CharField(max_length=50, unique=True)
    cus_idcard = models.CharField(max_length=50)
    cus_class = models.CharField(max_length=50, null=True)
    cus_sex = models.CharField(max_length=50, null=True)
    cus_phone1 = models.CharField(max_length=50)
    cus_phone2 = models.CharField(max_length=50, null=True)
    cus_addr1 = models.CharField(max_length=50)
    cus_addr2 = models.CharField(max_length=50)
    cus_email = models.CharField(max_length=50, null=True)
    cus_bd = models.CharField(max_length=50)
    cus_shop_id = models.CharField(max_length=50)
    cus_arr_date = models.CharField(max_length=50)

    cus_source = models.CharField(max_length=50, null=True)
    cus_remark = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.cus_name