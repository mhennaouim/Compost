# Generated by Django 4.1.6 on 2023-05-06 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GreenersAccount', '0006_delete_compost'),
    ]

    operations = [
        migrations.AddField(
            model_name='greener',
            name='ComposterStatus',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('accepted', 'Accepted')], default='waiting', max_length=50),
        ),
    ]
