# Generated by Django 3.0.7 on 2020-10-04 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Cart_json',
            field=models.TextField(blank=True, null=True),
        ),
    ]