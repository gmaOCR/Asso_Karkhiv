# Generated by Django 4.2.7 on 2023-12-14 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0008_concretephoto'),
        ('projects', '0007_project_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='thumbnail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_thumbnail', to='gallery.photoproject'),
        ),
    ]
