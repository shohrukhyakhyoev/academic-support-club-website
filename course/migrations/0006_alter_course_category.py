# Generated by Django 4.1.5 on 2023-01-16 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_category_course_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.category'),
        ),
    ]
