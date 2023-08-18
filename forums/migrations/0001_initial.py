# Generated by Django 3.2 on 2023-08-04 16:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forum_name', models.CharField(max_length=100, unique=True)),
                ('about', models.TextField(max_length=100)),
                ('visibility', models.CharField(choices=[('Open', 'OPEN'), ('Restricted', 'RESTRICTED')], default='Open', max_length=50)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('category', models.ManyToManyField(blank=True, related_name='forum_category', to='forums.Category')),
                ('members', models.ManyToManyField(related_name='forum_members', to=settings.AUTH_USER_MODEL)),
                ('moderator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='forum_mod', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='Guidelines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.CharField(max_length=100)),
                ('forum', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='forum_rules', to='forums.forum')),
            ],
        ),
    ]