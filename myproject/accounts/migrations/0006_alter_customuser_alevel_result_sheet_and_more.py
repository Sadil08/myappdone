# Generated by Django 5.1.1 on 2024-10-21 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_paperupload_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='alevel_result_sheet',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='nic_photo',
            field=models.ImageField(upload_to=''),
        ),
    ]
