# Generated by Django 3.1 on 2020-12-16 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitnesspal', '0013_auto_20201216_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calories',
            name='unit',
            field=models.CharField(default='', max_length=100),
        ),
    ]
