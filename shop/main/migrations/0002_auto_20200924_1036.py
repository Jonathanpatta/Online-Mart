# Generated by Django 3.0.7 on 2020-09-24 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='imgs'),
        ),
    ]
