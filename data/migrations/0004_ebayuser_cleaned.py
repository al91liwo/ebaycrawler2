# Generated by Django 3.1.1 on 2020-09-25 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20200925_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebayuser',
            name='cleaned',
            field=models.BooleanField(default=False),
        ),
    ]
