# Generated by Django 5.0.2 on 2024-03-11 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comps', '0005_alter_complaint_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='closed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
