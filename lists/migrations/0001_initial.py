# Generated by Django 4.0.4 on 2022-06-17 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='')),
                ('list', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='lists.list')),
            ],
            options={
                'ordering': ('id',),
                'unique_together': {('list', 'text')},
            },
        ),
    ]
