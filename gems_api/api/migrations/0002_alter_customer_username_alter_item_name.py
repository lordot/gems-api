# Generated by Django 4.2.3 on 2023-07-28 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='username',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
