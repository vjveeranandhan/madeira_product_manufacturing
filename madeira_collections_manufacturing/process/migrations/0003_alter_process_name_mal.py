# Generated by Django 5.1.4 on 2025-01-05 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0002_rename_process_name_process_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='name_mal',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
