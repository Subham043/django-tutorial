# Generated by Django 4.1.7 on 2023-02-21 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_rename_post_for_article_article_for'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=250, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField()),
                ('approved_by_admin', models.BooleanField(default=False)),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogs.article')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=250, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reply', models.TextField()),
                ('approved_by_admin', models.BooleanField(default=False)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogs.comment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]