# Generated by Django 4.0.3 on 2024-03-27 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screen', '0016_alter_seatingconfiguration_theater'),
    ]

    operations = [
        migrations.RenameField(
            model_name='show',
            old_name='price',
            new_name='avgP',
        ),
        migrations.AddField(
            model_name='show',
            name='maxP',
            field=models.DecimalField(decimal_places=2, default=200, max_digits=6),
        ),
        migrations.AddField(
            model_name='show',
            name='minP',
            field=models.DecimalField(decimal_places=2, default=120, max_digits=6),
        ),
    ]