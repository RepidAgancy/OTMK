# Generated by Django 4.2 on 2024-12-23 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='developers',
            new_name='programmers',
        ),
    ]
