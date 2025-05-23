# Generated by Django 4.2.4 on 2023-08-16 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='functionversion',
            name='build_logs',
            field=models.FileField(blank=True, null=True, upload_to='functions/'),
        ),
        migrations.AlterField(
            model_name='functionversion',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('STARTED', 'Started'), ('RUNNING', 'Running'), ('UNKNOWN', 'Unknown'), ('SUCCEEDED', 'Succeeded'), ('FAILED', 'Failed')], default='PENDING', max_length=20),
        ),
    ]
