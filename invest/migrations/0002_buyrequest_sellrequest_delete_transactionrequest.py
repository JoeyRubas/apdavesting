# Generated by Django 5.0 on 2025-01-29 03:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='buyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shares', models.DecimalField(decimal_places=2, max_digits=10)),
                ('votes', models.IntegerField()),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invest.ticker')),
            ],
        ),
        migrations.CreateModel(
            name='sellRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shares', models.DecimalField(decimal_places=2, max_digits=10)),
                ('votes', models.IntegerField()),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invest.position')),
            ],
        ),
        migrations.DeleteModel(
            name='transactionRequest',
        ),
    ]
