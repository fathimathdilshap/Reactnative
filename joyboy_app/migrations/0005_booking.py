# Generated by Django 4.1.4 on 2024-01-15 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joyboy_app', '0004_rename_post_category_id_posts_post_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('phone_number', models.BigIntegerField()),
                ('adress', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
    ]
