# Generated by Django 5.1.4 on 2025-01-12 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_message_file_profile_delete_membership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_seen',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
