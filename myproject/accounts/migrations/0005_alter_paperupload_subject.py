# Generated by Django 5.1.1 on 2024-10-15 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paperupload',
            name='subject',
            field=models.CharField(choices=[('physics', 'Physics'), ('cmath', 'Combined Maths'), ('chemistry', 'Chemistry'), ('biology', 'Biology'), ('accounting', 'Accounting'), ('ict', 'ICT'), ('science', 'O/L-Science'), ('olmaths', 'O/L-Maths'), ('english', 'English')], max_length=100),
        ),
    ]
