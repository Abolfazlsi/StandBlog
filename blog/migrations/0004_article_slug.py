# Generated by Django 5.0.6 on 2024-06-27 21:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_delete_new"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="slug",
            field=models.SlugField(null=True, unique=True),
        ),
    ]
