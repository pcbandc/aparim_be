# Generated by Django 5.0.1 on 2024-06-24 12:09

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_stockcard_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='posted',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='goodtransaction',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='stock.stockcard'),
        ),
        migrations.AlterField(
            model_name='goodtransaction',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='stock.document'),
        ),
        migrations.AlterField(
            model_name='goodtransaction',
            name='good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='stock.good'),
        ),
        migrations.AlterField(
            model_name='goodtransaction',
            name='transaction_type',
            field=models.CharField(choices=[('RT', 'Receipt'), ('DH', 'Dispatch'), ('CN', 'Credit note'), ('DN', 'Debit note'), ('WO', 'Write off'), ('MG', 'Moving goods')], max_length=12),
        ),
        migrations.AlterField(
            model_name='stockcard',
            name='good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='stock.good'),
        ),
        migrations.AlterField(
            model_name='stockcard',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 24, 15, 9, 16, 142074)),
        ),
        migrations.AlterField(
            model_name='stockcard',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='stock.warehouse'),
        ),
    ]
