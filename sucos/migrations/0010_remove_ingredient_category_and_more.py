# Generated by Django 5.0 on 2025-04-24 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sucos', '0009_categoryingredient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='category',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='category_ingredient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='ingredientes', to='sucos.categoryingredient', verbose_name='Categoria'),
            preserve_default=False,
        ),
    ]
