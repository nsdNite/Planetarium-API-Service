# Generated by Django 4.1 on 2024-01-27 17:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("planetarium_api", "0002_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="astronomyshow",
            old_name="show_theme",
            new_name="show_themes",
        ),
    ]
