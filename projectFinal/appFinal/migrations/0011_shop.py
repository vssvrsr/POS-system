# Generated by Django 2.2.6 on 2019-10-26 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFinal', '0010_auto_20191025_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_id', models.CharField(max_length=50, unique=True)),
                ('shop_name', models.CharField(max_length=50)),
                ('shop_class', models.CharField(max_length=50)),
                ('shop_addr', models.CharField(max_length=50)),
                ('shop_phone1', models.CharField(max_length=50)),
                ('shop_phone2', models.CharField(max_length=50, null=True)),
                ('shop_remark', models.CharField(max_length=300, null=True)),
            ],
        ),
    ]
