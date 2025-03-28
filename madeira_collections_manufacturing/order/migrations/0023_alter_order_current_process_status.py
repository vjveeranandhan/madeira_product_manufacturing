# Generated by Django 5.1.4 on 2025-01-25 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0022_order_current_process_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="current_process_status",
            field=models.CharField(
                choices=[
                    ("initiated", "Initiated"),
                    ("requested", "Requested"),
                    ("on_going", "On going"),
                    ("completed", "Completed"),
                ],
                default="requested",
                help_text="Status of current process",
                max_length=20,
            ),
        ),
    ]
