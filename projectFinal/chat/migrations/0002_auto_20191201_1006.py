# Generated by Django 2.2.6 on 2019-12-01 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='shop_id',
            new_name='group_name',
        ),
    ]
