# Generated by Django 4.2.4 on 2023-08-29 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0004_alter_functionversion_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='function',
            name='source_location',
            field=models.TextField(blank=True, null=True),
        ),
    ]
