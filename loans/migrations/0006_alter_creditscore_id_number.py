# Generated by Django 4.1.3 on 2023-05-09 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0005_alter_creditscore_agent_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditscore',
            name='id_number',
            field=models.IntegerField(unique=True),
        ),
    ]
