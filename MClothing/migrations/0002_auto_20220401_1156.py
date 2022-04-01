# Generated by Django 3.2.7 on 2022-04-01 06:11

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MClothing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, null=True, unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('code', models.CharField(editable=False, max_length=16, unique=True)),
                ('publish_date', models.DateField(default=datetime.date.today)),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='ImageAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True)),
                ('thumbnail', models.URLField(null=True)),
                ('slug', models.SlugField()),
                ('product_code', models.CharField(editable=False, max_length=16, null=True, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('is_active', models.BooleanField(default=True, help_text='if set active, then it will be visible in the website.')),
                ('published_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MClothing.customer')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='MClothing.category')),
            ],
            options={
                'verbose_name_plural': 'Products',
                'ordering': ('-title',),
            },
        ),
        migrations.DeleteModel(
            name='UniqueRandom',
        ),
        migrations.AddField(
            model_name='imagealbum',
            name='product',
            field=models.ForeignKey(help_text='Provide a url of image', null=True, on_delete=django.db.models.deletion.CASCADE, to='MClothing.product', verbose_name='Images'),
        ),
    ]
