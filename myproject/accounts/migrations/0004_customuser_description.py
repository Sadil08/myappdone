# Generated by Django 5.1.1 on 2024-10-15 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='description',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
