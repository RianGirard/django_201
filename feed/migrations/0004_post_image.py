# Generated by Django 2.2 on 2021-07-12 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='default.png', upload_to=''),
        ),
    ]
