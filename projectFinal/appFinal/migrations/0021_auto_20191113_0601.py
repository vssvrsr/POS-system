# Generated by Django 2.2.6 on 2019-11-13 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appFinal', '0020_sale_salealloc_salestock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='sale_cus_id',
            new_name='sale_cus',
        ),
        migrations.RenameField(
            model_name='sale',
            old_name='sale_shop_id',
            new_name='sale_shop',
        ),
        migrations.RenameField(
            model_name='salealloc',
            old_name='salealloc_sale_id',
            new_name='salealloc_sale',
        ),
        migrations.RenameField(
            model_name='salealloc',
            old_name='salealloc_stock_id',
            new_name='salealloc_stock',
        ),
        migrations.RenameField(
            model_name='salestock',
            old_name='salestock_sale_id',
            new_name='salestock_sale',
        ),
        migrations.RenameField(
            model_name='salestock',
            old_name='salestock_stock_id',
            new_name='salestock_stock',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='sale_created_by_user_id',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='sale_modified_by_user_id',
        ),
        migrations.AddField(
            model_name='sale',
            name='sale_created_by_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_by_this_user', to='appFinal.User'),
        ),
        migrations.AddField(
            model_name='sale',
            name='sale_modified_by_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_by_this_user', to='appFinal.User'),
        ),
    ]
