# Generated by Django 5.0.6 on 2024-06-08 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0002_scheduledtask'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmanager',
            name='fixed',
            field=models.BooleanField(default=False, help_text='True if any inconsistence was fixed'),
        ),
    ]
