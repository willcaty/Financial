# Generated by Django 2.0.5 on 2018-07-16 11:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QIMAN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=10)),
                ('PE_PB', models.IntegerField()),
                ('percentile', models.IntegerField(blank=True)),
                ('high', models.IntegerField()),
                ('low', models.IntegerField()),
                ('roe', models.IntegerField()),
                ('color', models.TextField(max_length=20)),
                ('date', models.DateField(default=datetime.date.today, unique=True)),
            ],
        ),
    ]
