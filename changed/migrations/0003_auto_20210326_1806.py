# Generated by Django 3.1.6 on 2021-03-26 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changed', '0002_businesscomments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businesscomments',
            name='body',
        ),
        migrations.AddField(
            model_name='businessinfo',
            name='body',
            field=models.TextField(default=''),
        ),
    ]
