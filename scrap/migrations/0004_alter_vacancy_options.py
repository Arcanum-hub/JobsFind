# Generated by Django 3.2.13 on 2022-05-28 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0003_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacancy',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Вакансия', 'verbose_name_plural': 'Вакансии'},
        ),
    ]
