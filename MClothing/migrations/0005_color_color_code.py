# Generated by Django 3.2.7 on 2022-04-01 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MClothing', '0004_auto_20220401_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='color_code',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
