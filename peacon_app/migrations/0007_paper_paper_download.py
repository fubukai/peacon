# Generated by Django 3.0.7 on 2021-10-14 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peacon_app', '0006_paper_paper_reward'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='Paper_download',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
