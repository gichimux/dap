# Generated by Django 3.2 on 2023-09-15 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_alter_post_topic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replylike',
            name='comment',
        ),
        migrations.AddField(
            model_name='replylike',
            name='reply',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reply_likes', to='posts.reply'),
            preserve_default=False,
        ),
    ]