# Generated by Django 4.2.3 on 2023-08-09 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaner', '0004_employeerange'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeCountScoring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('low_threshold', models.IntegerField()),
                ('low_score', models.IntegerField(help_text='Score for companies Low employee count threshold or greater')),
                ('mid_threshold', models.IntegerField()),
                ('mid_score', models.IntegerField(help_text='Score for companies matching Mid employee count threshold or greater')),
                ('high_threshold', models.IntegerField()),
                ('high_score', models.IntegerField(help_text='Score for companies matching High employee count or greater')),
            ],
        ),
        migrations.DeleteModel(
            name='EmployeeRange',
        ),
    ]