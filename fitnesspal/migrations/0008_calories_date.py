# Generated by Django 3.1 on 2020-11-22 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitnesspal', '0007_auto_20201122_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='calories',
            name='date',
            field=models.DateTimeField(null=True, verbose_name='date food added'),
        ),
    ]
