# Generated by Django 4.2.7 on 2024-01-06 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0020_vol'),
    ]

    operations = [
        migrations.AddField(
            model_name='voyage',
            name='vol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.vol'),
            preserve_default=False,
        ),
    ]
