# Generated by Django 2.1 on 2019-03-15 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_category_judges'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='can_anyone_judge',
        ),
    ]
