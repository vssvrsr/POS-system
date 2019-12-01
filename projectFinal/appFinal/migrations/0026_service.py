# Generated by Django 2.2.6 on 2019-11-21 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appFinal', '0025_auto_20191114_0924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serv_id', models.CharField(max_length=50)),
                ('serv_date', models.CharField(max_length=50)),
                ('serv_stock_price', models.IntegerField()),
                ('serv_price', models.IntegerField()),
                ('serv_point', models.IntegerField()),
                ('serv_pay', models.CharField(max_length=50)),
                ('serv_type', models.CharField(max_length=50)),
                ('serv_shop_id', models.CharField(max_length=50)),
                ('serv_remark', models.CharField(max_length=50)),
                ('serv_complete', models.BooleanField(default=False)),
                ('serv_created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create_by_this_user_serv', to='appFinal.User')),
                ('serv_cus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFinal.Customer')),
                ('serv_emp1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serv_by_emp1', to='appFinal.Employee')),
                ('serv_emp2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serv_by_emp2', to='appFinal.Employee')),
                ('serv_emp3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serv_by_emp3', to='appFinal.Employee')),
                ('serv_modified_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modified_by_this_user_serv', to='appFinal.User')),
                ('serv_person_in_charge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFinal.Employee')),
                ('serv_stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFinal.Stock')),
            ],
        ),
    ]