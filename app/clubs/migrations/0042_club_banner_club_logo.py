# Generated by Django 4.2.23 on 2025-07-11 23:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("clubs", "0041_remove_club_banner_remove_club_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="club",
            name="banner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="clubs.clubfile",
            ),
        ),
        migrations.AddField(
            model_name="club",
            name="logo",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="clubs.clubfile",
            ),
        ),
    ]
