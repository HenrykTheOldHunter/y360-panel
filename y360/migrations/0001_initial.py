# Generated by Django 4.2.5 on 2023-09-08 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.IntegerField(help_text='department ID', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='department name', max_length=200)),
                ('parentId', models.IntegerField(help_text='parent ID')),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.IntegerField(help_text='group ID', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='group name', max_length=200)),
                ('parentId', models.IntegerField(help_text='parent ID')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.IntegerField(help_text='personal ID', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='full name', max_length=200)),
                ('email', models.CharField(help_text='personal email', max_length=200)),
                ('departmentId', models.IntegerField(help_text='ID of department')),
                ('role', models.CharField(help_text='Staff or Bot or Admin', max_length=100)),
                ('img', models.IntegerField(help_text='Ico ID from yandex')),
            ],
        ),
        migrations.CreateModel(
            name='Groups_Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='y360.groups')),
                ('staffId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='y360.staff')),
            ],
        ),
    ]
