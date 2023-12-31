# Generated by Django 3.0.7 on 2021-09-29 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('peacon_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='Paper_rating',
        ),
        migrations.AddField(
            model_name='paper',
            name='Paper_like',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.CreateModel(
            name='like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=10, null=True)),
                ('papers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='papers', to='peacon_app.Paper')),
            ],
        ),
    ]
