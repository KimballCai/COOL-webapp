# Generated by Django 4.1.7 on 2023-06-15 23:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('set_id', models.AutoField(primary_key=True, serialize=False)),
                ('set_name', models.CharField(max_length=50)),
                ('set_details', models.CharField(max_length=500)),
                ('cube_name', models.CharField(max_length=50)),
                ('cube_size', models.FloatField()),
                ('num_records', models.IntegerField(default=0)),
                ('num_ids', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('save_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='upload_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_save', models.CharField(max_length=50)),
                ('save_time', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('query_id', models.AutoField(primary_key=True, serialize=False)),
                ('query_name', models.CharField(max_length=50)),
                ('query_mode', models.CharField(choices=[('CC', 'Cohort-Create'), ('CA', 'Cohort-Analysis'), ('OS', 'Others')], default='OS', max_length=2)),
                ('save_time', models.DateTimeField(auto_now=True)),
                ('exe_time', models.FloatField()),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('set_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cool_dashboard.dataset')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('query_name', 'user_id', 'set_id')},
            },
        ),
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('cohort_id', models.AutoField(primary_key=True, serialize=False)),
                ('cohort_size', models.FloatField()),
                ('cohort_name', models.CharField(max_length=20)),
                ('save_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('query_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cool_dashboard.query')),
                ('set_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cool_dashboard.dataset')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('analysis_id', models.AutoField(primary_key=True, serialize=False)),
                ('analysis_name', models.CharField(max_length=50)),
                ('analysis_save', models.CharField(max_length=50)),
                ('analysis_type', models.CharField(max_length=50)),
                ('save_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('set_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cool_dashboard.dataset')),
            ],
        ),
    ]