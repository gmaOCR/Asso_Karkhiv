# Generated by Django 4.2.7 on 2023-12-05 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_photos_alter_project_place'),
        ('members', '0003_alter_member_photo_alter_member_projects'),
    ]

    operations = [
        migrations.CreateModel(
            name='NonMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('projects', models.ManyToManyField(blank=True, related_name='non_members', to='projects.project')),
            ],
        ),
    ]
