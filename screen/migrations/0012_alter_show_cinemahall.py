# Generated by Django 4.0.3 on 2024-02-24 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('screen', '0011_remove_seat_show_remove_showdate_show_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='cinemahall',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shows', to='screen.cinemahall'),
        ),
    ]
