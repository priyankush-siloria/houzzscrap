# Generated by Django 2.2.2 on 2019-06-28 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interior_app', '0005_auto_20190625_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationdata',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='interior_app.Locations'),
        ),
    ]
