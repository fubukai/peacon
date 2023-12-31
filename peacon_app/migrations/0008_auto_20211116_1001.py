# Generated by Django 3.0.7 on 2021-11-16 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peacon_app', '0007_paper_paper_download'),
    ]

    operations = [
        migrations.CreateModel(
            name='Speaker_user',
            fields=[
                ('PK_Exuser', models.AutoField(primary_key=True, serialize=False)),
                ('Speaker_type', models.CharField(max_length=100, null=True)),
                ('Speaker_name', models.CharField(max_length=100, null=True)),
                ('Speaker_lastname', models.CharField(max_length=100, null=True)),
                ('Speaker_position', models.CharField(max_length=100, null=True)),
                ('Speaker_Ageny', models.CharField(max_length=100, null=True)),
                ('Speaker_email', models.CharField(max_length=25, null=True)),
                ('Speaker_line', models.CharField(max_length=25, null=True)),
                ('Speaker_tel', models.CharField(max_length=12, null=True)),
                ('Speaker_address', models.TextField(null=True)),
                ('Speaker_password', models.CharField(max_length=25, null=True)),
                ('Speaker_Status', models.CharField(max_length=25, null=True)),
                ('Speaker_Userid', models.CharField(max_length=25, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='surveys',
            name='survey_id',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
