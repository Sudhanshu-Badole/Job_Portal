# Generated by Django 3.0 on 2023-08-02 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_jobapplication'),
    ]

    operations = [
        migrations.DeleteModel(
            name='JobApplication',
        ),
    ]