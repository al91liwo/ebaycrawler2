# Generated by Django 3.1.1 on 2020-09-29 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20200929_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachmenttemplate',
            name='attachment',
            field=models.FileField(upload_to=''),
        ),
    ]