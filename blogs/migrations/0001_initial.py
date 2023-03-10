# Generated by Django 4.1.7 on 2023-02-21 08:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('post_for', models.CharField(choices=[('FOR_KIDS', 'Kids'), ('FOR_ADULTS', 'Adults')], default='FOR_ADULTS', max_length=50)),
                ('banner', models.ImageField(upload_to='post_banners')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('publish_on', models.DateField(blank=True, default=datetime.date.today)),
            ],
        ),
    ]
