# Generated by Django 4.0.4 on 2022-05-11 19:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0007_alter_expense_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 5, 11, 19, 11, 59, 171383, tzinfo=utc)),
        ),
    ]
