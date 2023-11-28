# Generated by Django 4.2.7 on 2023-11-28 12:20

from django.db import migrations, models
import members.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=members.models.user_photo_upload_filename)),
                ('biography', models.TextField()),
                ('projects', models.ManyToManyField(related_name='members', to='projects.project')),
            ],
        ),
    ]
