# Generated by Django 5.1.1 on 2024-09-22 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0002_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='phone',
            field=models.PositiveBigIntegerField(max_length=10),
        ),
    ]