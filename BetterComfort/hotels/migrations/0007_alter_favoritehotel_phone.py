# Generated by Django 5.1.3 on 2024-12-11 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0006_favoritehotel_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritehotel',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
