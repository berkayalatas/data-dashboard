# Generated by Django 4.0.4 on 2022-05-07 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='sex',
            field=models.PositiveIntegerField(choices=[(0, 'Female'), (1, 'Male')], null=True),
        ),
    ]
