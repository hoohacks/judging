# Generated by Django 2.1 on 2019-03-16 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20190316_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sd_offset',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=9, null=True),
        ),
    ]
