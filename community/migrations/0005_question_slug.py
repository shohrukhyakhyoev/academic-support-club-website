# Generated by Django 4.1.5 on 2023-03-13 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_alter_question_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='slug',
            field=models.SlugField(default='slug'),
        ),
    ]
