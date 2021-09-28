# Generated by Django 3.2.7 on 2021-09-28 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_sis', '0002_remove_lookupcodetype_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activityattendee',
            old_name='user_role',
            new_name='attendee_type',
        ),
        migrations.AddField(
            model_name='activityattendee',
            name='is_organiser',
            field=models.BooleanField(default=False),
        ),
    ]
