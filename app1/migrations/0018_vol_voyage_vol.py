# Generated by Django 4.2.7 on 2024-01-06 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0017_delete_vol'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_depart', models.DateField()),
                ('date_arrive', models.DateField()),
                ('compagnie', models.CharField(max_length=100)),
                ('classe', models.CharField(choices=[('eco', 'economie'), ('bsn', 'bisness')], max_length=100)),
                ('escale', models.CharField(max_length=100)),
                ('ville_arrive', models.CharField(max_length=100)),
                ('ville_depart', models.CharField(max_length=100)),
                ('nbr_heure', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='voyage',
            name='vol',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app1.vol'),
            preserve_default=False,
        ),
    ]
