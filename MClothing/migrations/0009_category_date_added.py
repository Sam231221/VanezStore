# Generated by Django 3.2.7 on 2022-04-08 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MClothing', '0008_alter_productreview_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='date_added',
            field=models.DateTimeField(null=True),
        ),
    ]
