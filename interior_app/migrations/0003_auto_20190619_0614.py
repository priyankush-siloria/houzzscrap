# Generated by Django 2.2.2 on 2019-06-19 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interior_app', '0002_locationdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationdata',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]