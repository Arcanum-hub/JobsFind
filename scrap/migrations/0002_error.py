# Generated by Django 3.2.13 on 2022-05-28 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('data', models.JSONField()),
            ],
        ),
    ]
