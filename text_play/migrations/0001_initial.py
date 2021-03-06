# Generated by Django 3.0.3 on 2021-06-05 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('keyword', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=2090, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mapping_of_url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='text_play.Keyword')),
                ('url_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='text_play.Url')),
            ],
        ),
    ]
