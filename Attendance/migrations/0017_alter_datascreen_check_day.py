# Generated by Django 3.2.4 on 2021-06-30 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0016_alter_register_register_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datascreen',
            name='check_day',
            field=models.CharField(max_length=10, null=True, verbose_name='请假天数'),
        ),
    ]