# Generated by Django 4.1.4 on 2022-12-09 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mc_donalds', '0002_alter_productorder_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='mc_donalds.staff'),
        ),
    ]
