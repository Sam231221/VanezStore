# Generated by Django 3.2.7 on 2022-04-02 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MClothing', '0007_productreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='review_rating',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=150),
        ),
    ]
