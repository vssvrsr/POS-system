# Generated by Django 2.2.6 on 2019-11-14 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appFinal', '0022_sale_sale_complete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salealloc',
            name='salealloc_point',
        ),
        migrations.RemoveField(
            model_name='salealloc',
            name='salealloc_stock',
        ),
    ]