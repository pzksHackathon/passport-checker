# Generated by Django 4.0.3 on 2022-03-07 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_alter_record_number_alter_record_series'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='record',
            unique_together={('series', 'number')},
        ),
    ]
