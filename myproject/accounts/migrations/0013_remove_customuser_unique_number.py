# Generated by Django 5.1.1 on 2024-11-05 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_customuser_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='unique_number',
        ),
    ]
