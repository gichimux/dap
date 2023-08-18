# Generated by Django 3.2 on 2023-08-11 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0007_remove_post_label'),
    ]

    operations = [
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.URLField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='parent',
        ),
        migrations.AlterField(
            model_name='reply',
            name='reply_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='hashtag',
            field=models.ManyToManyField(blank=True, related_name='hash_tag', to='posts.HashTag'),
        ),
    ]