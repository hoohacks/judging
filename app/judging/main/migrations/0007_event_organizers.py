# Generated by Django 2.1 on 2019-03-13 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_category_min_judges'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='organizers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Organization'),
        ),
    ]
