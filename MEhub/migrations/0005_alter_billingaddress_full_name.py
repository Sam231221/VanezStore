# Generated by Django 3.2.7 on 2022-05-19 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MEhub', '0004_auto_20220519_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='full_name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
