# Generated by Django 3.1.4 on 2021-02-13 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_student_strand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='numeric_grade',
            field=models.SmallIntegerField(default=0, verbose_name='Grade'),
        ),
    ]
