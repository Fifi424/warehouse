# Generated by Django 4.2.7 on 2024-12-14 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_returneditem_purchaseditem'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='issued',
            field=models.BooleanField(default=False),
        ),
    ]
