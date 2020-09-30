# Generated by Django 3.1.1 on 2020-09-29 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20200927_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachmentTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(upload_to='attachment')),
            ],
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=25)),
                ('text', models.CharField(max_length=5000)),
            ],
        ),
        migrations.DeleteModel(
            name='Blacklist',
        ),
    ]