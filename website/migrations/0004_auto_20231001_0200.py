# Generated by Django 3.2.21 on 2023-09-30 21:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_productdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='distributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=1000000000, null=True)),
                ('lat_name', models.CharField(max_length=1000000000, null=True)),
                ('email', models.CharField(max_length=1000000000, null=True)),
                ('phone', models.CharField(max_length=1000000000, null=True)),
                ('country', models.CharField(max_length=1000000000, null=True)),
                ('company', models.CharField(max_length=1000000000, null=True)),
                ('staff', models.CharField(max_length=1000000000, null=True)),
                ('website', models.CharField(max_length=1000000000, null=True)),
                ('comment', models.CharField(max_length=1000000000, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='newsletter',
            name='ndate',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
