# Generated by Django 3.2.4 on 2021-07-10 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_auto_20210630_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='<django.db.models.fields.CharField>/qr_codes/'),
        ),
        migrations.AlterField(
            model_name='videos',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='<django.db.models.fields.CharField>/videos/'),
        ),
    ]
