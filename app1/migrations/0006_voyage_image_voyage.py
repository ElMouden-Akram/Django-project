# Generated by Django 4.2.7 on 2024-01-04 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_alter_client_client_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='voyage',
            name='image_voyage',
            field=models.ImageField(blank=True, default='voyagepic.png', null=True, upload_to=''),
        ),
    ]
