# Generated by Django 2.0.7 on 2018-07-13 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0008_auto_20180710_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='filename_tag',
            field=models.TextField(blank=True),
        ),
    ]