# Generated by Django 2.1.5 on 2019-02-24 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment_content',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='comment_time',
            new_name='created_time',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='comment_user',
            new_name='user',
        ),
    ]
