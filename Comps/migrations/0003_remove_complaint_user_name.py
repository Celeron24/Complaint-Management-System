# Generated by Django 5.0.2 on 2024-03-07 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comps', '0002_alter_complaint_complaint_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='user_name',
        ),
    ]
