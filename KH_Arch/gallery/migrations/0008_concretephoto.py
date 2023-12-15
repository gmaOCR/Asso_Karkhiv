# Generated by Django 4.2.7 on 2023-12-14 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0007_alter_photoevent_image_alter_photoevent_thumbnail_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConcretePhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='photos/')),
                ('thumbnail', models.ImageField(editable=False, upload_to='thumbnails/')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]