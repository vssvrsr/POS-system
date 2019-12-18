# Generated by Django 2.2.6 on 2019-12-17 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appFinal', '0032_commincometype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salaryresult',
            name='SRSCIncome',
        ),
        migrations.RemoveField(
            model_name='salaryresult',
            name='SRSCIncomeComm',
        ),
        migrations.RemoveField(
            model_name='salaryresult',
            name='SR_emp_name',
        ),
        migrations.RemoveField(
            model_name='salaryresult',
            name='SR_income',
        ),
        migrations.RemoveField(
            model_name='salaryresult',
            name='SR_point',
        ),
        migrations.RemoveField(
            model_name='salaryresult',
            name='SR_point1',
        ),
        migrations.RemoveField(
            model_name='salaryresult',
            name='SR_point2',
        ),
        migrations.RemoveField(
            model_name='salaryresult',
            name='SR_point3',
        ),
        migrations.RemoveField(
            model_name='salaryresult',
            name='SR_salary',
        ),
        migrations.RemoveField(
            model_name='salaryresult',
            name='SR_stock_income_comm',
        ),
        migrations.RemoveField(
            model_name='salaryresult',
            name='SRbarberIncome',
        ),
        migrations.RemoveField(
            model_name='salaryresult',
            name='SRbarberIncomeComm',
        ),
        migrations.RemoveField(
            model_name='salaryresult',
            name='SRresult',
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='SR_emp',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appFinal.Employee'),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='SR_result',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='hair_income_all',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='hair_income_all_comm',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='hair_income_all_emp1',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='hair_income_all_emp2',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='hair_income_all_emp3',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='hair_point_all_emp1',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='hair_point_all_emp2',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='hair_point_all_emp3',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='head_income_all',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='head_income_all_comm',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='head_income_all_emp1',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='head_income_all_emp2',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='head_income_all_emp3',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='head_point_all_emp1',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='head_point_all_emp2',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='head_point_all_emp3',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='stock_income_all',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='stock_income_all_comm',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salaryresult',
            name='stock_point_all',
            field=models.IntegerField(null=True),
        ),
    ]