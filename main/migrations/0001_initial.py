# Generated by Django 4.2.7 on 2024-12-11 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=50, unique=True)),
                ('sender_name', models.CharField(max_length=100)),
                ('sender_contact', models.CharField(max_length=20)),
                ('creation_date', models.DateField()),
                ('total_weight', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PvzLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('rent_paid_until', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('item_weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='pvz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='main.pvzlocation'),
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_status', models.CharField(choices=[('Оплачен', 'Оплачен'), ('Предоплачен', 'Предоплачен'), ('Требуется', 'Требуется')], max_length=20)),
                ('recipient_name', models.CharField(max_length=100)),
                ('recipient_contact', models.CharField(max_length=20)),
                ('acceptance_date', models.DateField()),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='delivery', to='main.order')),
            ],
        ),
    ]