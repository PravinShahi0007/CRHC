# Generated by Django 3.2.4 on 2021-06-29 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0009_auto_20210629_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datascreen',
            name='check_state',
            field=models.CharField(default='N', max_length=10, verbose_name='标记'),
        ),
    ]