# Generated by Django 5.0.1 on 2024-08-03 10:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0014_alter_goodtransaction_document_line_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodtransaction',
            name='transaction_type',
            field=models.CharField(choices=[('RT', 'Receipt'), ('DH', 'Dispatch'), ('CN', 'Credit note'), ('DN', 'Debit note'), ('WO', 'Write off'), ('MT', 'Moving goods to'), ('MF', 'Moving goods from')], max_length=12),
        ),
        migrations.AlterField(
            model_name='stockcard',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 3, 13, 40, 45, 893738)),
        ),
    ]
