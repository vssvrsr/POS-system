# Generated by Django 2.2.6 on 2019-12-12 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFinal', '0030_commission_commlimit_multisevicepercent_regularbonus_salaryresult_salaryselectemp'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='comm_income_type',
            field=models.CharField(max_length=50, null=True),
        ),
    ]