# Generated by Django 4.1.5 on 2023-03-13 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0022_post_slug_alter_author_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
