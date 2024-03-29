# Generated by Django 3.2.7 on 2021-11-05 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UniqueRandom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(editable=False, max_length=16, unique=True)),
                ('test_data', models.CharField(max_length=128, verbose_name='Test Data')),
            ],
            options={
                'verbose_name': 'Unique Random',
                'verbose_name_plural': 'Unique Randoms',
            },
        ),
    ]
