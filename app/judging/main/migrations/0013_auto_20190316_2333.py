# Generated by Django 2.1 on 2019-03-16 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_user_sd_offset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sd_offset',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=9),
        ),
    ]
