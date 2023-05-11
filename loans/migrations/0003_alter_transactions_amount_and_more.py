# Generated by Django 4.1.3 on 2023-05-05 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0002_calculation_creditscore_alter_transactions_ref_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='ba_before',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Balance Before'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='bal_after',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Balance After'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='f_id',
            field=models.CharField(max_length=255, verbose_name='Transaction ID'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='fees',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Fees'),
        ),
    ]
