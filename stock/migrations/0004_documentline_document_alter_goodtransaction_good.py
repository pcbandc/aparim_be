# Generated by Django 5.0.1 on 2024-06-14 15:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_goodtransaction_good_alter_documentline_good'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentline',
            name='document',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='doc_documents', to='stock.document'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='goodtransaction',
            name='good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='stock.good'),
        ),
    ]
