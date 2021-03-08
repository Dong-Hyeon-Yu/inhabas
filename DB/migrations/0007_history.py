# Generated by Django 3.1.5 on 2021-03-08 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0006_useremail'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('history_no', models.AutoField(db_column='HISTORY_NO', primary_key=True, serialize=False)),
                ('history_cont', models.CharField(db_column='HISTORY_CONT', max_length=500)),
                ('history_date', models.DateTimeField(db_column='HISTORY_DATE')),
            ],
            options={
                'db_table': 'HISTORY',
                'managed': False,
            },
        ),
    ]
