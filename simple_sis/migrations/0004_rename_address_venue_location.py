# Generated by Django 3.2.7 on 2021-09-28 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_sis', '0003_auto_20210928_2014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venue',
            old_name='address',
            new_name='location',
        ),
    ]
