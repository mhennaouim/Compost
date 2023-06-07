# Generated by Django 4.1.6 on 2023-04-24 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GreenersAccount', '0004_greener_is_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CompostName', models.CharField(max_length=255)),
                ('CompostImage', models.ImageField(upload_to='composts/')),
                ('CompostType', models.CharField(choices=[('AnimalManure', 'Animal manure'), ('PlantFertilizers', 'Plant-based fertilizers'), ('BiodegradableFertilizers', 'Biodegradable fertilizers')], max_length=30)),
                ('CompostQuantity', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
