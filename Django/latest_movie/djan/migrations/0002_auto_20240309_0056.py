# Generated by Django 3.2.10 on 2024-03-08 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='trusted_director',
            fields=[
                ('director', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('average_audience', models.IntegerField(null=True)),
                ('audience_showcnt', models.IntegerField(null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='director',
        ),
    ]
