# Generated by Django 3.2.10 on 2024-03-08 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djan', '0003_auto_20240309_0256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trusted_actor',
            name='avg_audience',
        ),
        migrations.AddField(
            model_name='trusted_actor',
            name='average_audience',
            field=models.IntegerField(null=True),
        ),
    ]
