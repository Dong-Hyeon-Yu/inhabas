# Generated by Django 3.1.5 on 2021-02-18 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0004_userdeletefile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChiefCarrier',
            fields=[
                ('carrier_no', models.AutoField(db_column='CARRIER_NO', primary_key=True, serialize=False)),
                ('carrier_content', models.CharField(blank=True, db_column='CARRIER_CONTENT', max_length=300, null=True)),
            ],
            options={
                'db_table': 'CHIEF_CARRIER',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MajorInfo',
            fields=[
                ('major_no', models.AutoField(db_column='MAJOR_NO', primary_key=True, serialize=False)),
                ('major_colleage', models.CharField(db_column='MAJOR_COLLEAGE', max_length=10)),
                ('major_name', models.CharField(db_column='MAJOR_NAME', max_length=20, unique=True)),
            ],
            options={
                'db_table': 'MAJOR_INFO',
                'managed': False,
            },
        ),
    ]
