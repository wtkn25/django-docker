# Generated by Django 3.1.5 on 2021-04-01 04:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sample.company'),
        ),
    ]