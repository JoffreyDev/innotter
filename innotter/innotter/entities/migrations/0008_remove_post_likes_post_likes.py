# Generated by Django 4.1.7 on 2023-03-15 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0007_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, to='entities.post'),
        ),
    ]
