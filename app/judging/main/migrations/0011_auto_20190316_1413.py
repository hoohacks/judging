# Generated by Django 2.1 on 2019-03-16 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_category_can_anyone_judge'),
    ]

    operations = [
        migrations.AddField(
            model_name='demo',
            name='norm_score',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='demo',
            name='raw_score',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=9),
        ),
    ]
