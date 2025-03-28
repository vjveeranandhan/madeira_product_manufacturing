# Generated by Django 5.1.4 on 2025-01-05 06:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0002_material'),
        ('process', '0004_alter_process_name_mal'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_name_mal', models.TextField(blank=True, max_length=100, null=True)),
                ('product_description', models.TextField(blank=True, null=True)),
                ('product_description_mal', models.TextField(blank=True, null=True)),
                ('product_length', models.FloatField(help_text='Length in feet')),
                ('product_height', models.FloatField(help_text='Height in feel')),
                ('product_width', models.FloatField(help_text='Width in feet')),
                ('reference_image', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('finish', models.TextField(blank=True, null=True)),
                ('event', models.CharField(blank=True, help_text='Event associated, e.g., Wedding', max_length=100, null=True)),
                ('estimated_delivery_date', models.DateField(blank=True, null=True)),
                ('estimated_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('customer_name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=15)),
                ('whatsapp_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.TextField()),
                ('carpenter_work_hr', models.FloatField(blank=True, help_text='Work hours required', null=True)),
                ('carpenter_work_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('carpenter_work_completion_date', models.DateField(blank=True, null=True)),
                ('carpenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carpenter_products', to=settings.AUTH_USER_MODEL)),
                ('carpenter_workers', models.ManyToManyField(blank=True, related_name='carpenter_worker_products', to=settings.AUTH_USER_MODEL)),
                ('main_manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_products', to=settings.AUTH_USER_MODEL)),
                ('order_stage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_stage', to='process.process')),
                ('wood', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='inventory.material')),
            ],
        ),
    ]
