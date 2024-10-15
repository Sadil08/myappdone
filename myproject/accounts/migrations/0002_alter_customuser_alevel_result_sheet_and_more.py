# Generated by Django 5.1.1 on 2024-10-14 07:40

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='alevel_result_sheet',
            field=models.ImageField(default='default_result_sheet.png', upload_to=accounts.models.user_directory_path),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='district',
            field=models.CharField(choices=[('colombo', 'Colombo'), ('gampaha', 'Gampaha'), ('kandy', 'Kandy'), ('galle', 'Galle'), ('matara', 'Matara'), ('jaffna', 'Jaffna'), ('kaluthara', 'Kaluthara'), ('kurunegala', 'Kurunegala'), ('matale', 'Matale')], default='Unknown', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(default='Unknown', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='medium',
            field=models.CharField(choices=[('english', 'English Medium'), ('sinhala', 'Sinhala Medium'), ('tamil', 'Tamil Medium')], default='Unknown', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='nic_photo',
            field=models.ImageField(default='default_result_sheet.png', upload_to=accounts.models.user_directory_path),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(default='Unknown', max_length=15),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='subject',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='town',
            field=models.CharField(default='Unknown', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='subject',
            field=models.ManyToManyField(to='accounts.subject'),
        ),
    ]