# Generated by Django 3.1.4 on 2021-02-13 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20210213_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='strand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.strand'),
        ),
    ]
