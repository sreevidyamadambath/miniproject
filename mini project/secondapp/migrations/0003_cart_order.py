# Generated by Django 4.2.6 on 2023-11-25 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('secondapp', '0002_alter_order_chef'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='secondapp.order'),
        ),
    ]
