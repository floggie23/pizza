# Generated by Django 2.2 on 2021-05-30 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myappfinal', '0003_auto_20210530_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
