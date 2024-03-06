# Generated by Django 5.0.2 on 2024-03-06 06:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comps', '0004_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='status',
            field=models.IntegerField(choices=[(1, 'InProgress'), (2, 'Solved')], default=1),
        ),
        migrations.AddField(
            model_name='complaint',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='Comp_Assign',
            field=models.CharField(choices=[('Complaint', 'Complaint'), ('Assignment', 'Assignment')], default='Complaint', max_length=50),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='user_name',
            field=models.CharField(max_length=20),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='complaint',
            name='assigned_employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Comps.employee'),
        ),
        migrations.DeleteModel(
            name='StaffUser',
        ),
    ]
