# Generated by Django 3.0.8 on 2020-07-23 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carcharger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_name', models.CharField(max_length=200)),
                ('car_chger_type', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sido_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Goo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goo_name', models.CharField(max_length=200)),
                ('sido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.Sido')),
            ],
        ),
    ]
