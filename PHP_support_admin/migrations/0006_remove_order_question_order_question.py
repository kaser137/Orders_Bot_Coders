# Generated by Django 4.1.7 on 2023-02-17 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PHP_support_admin', '0005_alter_order_client_alter_order_contractor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='question',
        ),
        migrations.AddField(
            model_name='order',
            name='question',
            field=models.ManyToManyField(blank=True, null=True, related_name='order', to='PHP_support_admin.question', verbose_name='question'),
        ),
    ]
