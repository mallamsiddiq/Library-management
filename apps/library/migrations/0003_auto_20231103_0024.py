# Generated by Django 3.0.5 on 2023-11-02 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20231031_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookissuance',
            name='active',
        ),
        migrations.AddField(
            model_name='bookissuance',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('pending', 'pending'), ('returned', 'returned')], default='active', max_length=30),
        ),
    ]
