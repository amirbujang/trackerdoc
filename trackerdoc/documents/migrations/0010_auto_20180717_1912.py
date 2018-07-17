# Generated by Django 2.0.7 on 2018-07-17 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0009_template_filename_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentstate',
            name='extra_data',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='template',
            name='filename_tag',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
