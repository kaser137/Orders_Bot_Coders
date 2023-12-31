# Generated by Django 4.1.7 on 2023-02-19 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PHP_support_admin', '0011_remove_order_question_question_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_opened',
            field=models.DateField(blank=True, null=True, verbose_name='date of opening the order by client'),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='tg_account',
            field=models.CharField(max_length=200, unique=True, verbose_name='telegram account of Contractor'),
        ),
    ]
