# Generated by Django 5.1.3 on 2024-12-20 20:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0008_remove_hotelrestro_city_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='hotels.hotelrestro')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('hotel', 'user')},
            },
        ),
    ]
