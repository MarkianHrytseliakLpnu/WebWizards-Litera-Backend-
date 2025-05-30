# Generated by Django 5.1.2 on 2024-11-03 22:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('work_schedule', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('phone_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('publishing', models.CharField(max_length=100)),
                ('year_of_publication', models.PositiveIntegerField()),
                ('language', models.CharField(max_length=50)),
                ('number_of_pages', models.PositiveIntegerField()),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library_app.location')),
            ],
        ),
        migrations.CreateModel(
            name='TradeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_time', models.DateTimeField()),
                ('borrowed_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowed_books', to='library_app.book')),
                ('brought_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brought_books', to='library_app.book')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library_app.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('response', models.TextField()),
                ('writing_time', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.book')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.user')),
            ],
        ),
    ]
