# Generated by Django 2.2 on 2021-05-30 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myappfinal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.IntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='Price',
        ),
    ]
