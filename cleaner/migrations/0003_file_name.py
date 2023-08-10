# Generated by Django 4.2.3 on 2023-08-02 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaner', '0002_file_file_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(blank=True, help_text='User-defined name for the file', max_length=255, null=True),
        ),
    ]
