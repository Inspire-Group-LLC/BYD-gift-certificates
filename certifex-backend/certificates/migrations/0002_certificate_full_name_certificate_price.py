# Generated by Django 4.1.1 on 2023-11-19 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='full_name',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='certificate',
            name='price',
            field=models.FloatField(default=None),
        ),
    ]