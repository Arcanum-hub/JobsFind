# Generated by Django 3.2.13 on 2022-05-28 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'verbose_name': 'Пользователи', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
