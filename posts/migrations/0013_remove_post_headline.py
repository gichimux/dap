# Generated by Django 3.2 on 2023-09-14 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_auto_20230915_0047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='headline',
        ),
    ]