# Generated by Django 2.0.7 on 2018-07-17 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0011_state_extra_data_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenttablecolumn',
            name='css_class',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='state',
            name='extra_data_label',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
