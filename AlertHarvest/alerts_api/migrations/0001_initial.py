# Generated by Django 5.0 on 2024-02-01 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
                ('severity', models.CharField(choices=[('CRITICAL', 'Critical'), ('MAJOR', 'Major'), ('WARNING', 'Warning')], default='WARNING', max_length=15)),
                ('message', models.TextField()),
                ('source', models.TextField(max_length=255)),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('CLOSED', 'Closed'), ('ACKNOWLEDGED', 'Acknowledged'), ('EXPIRED', 'Expired')], default='OPEN', max_length=15)),
                ('acknowledged_at', models.DateTimeField(blank=True, null=True)),
                ('last_occurrence', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('blackout', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BlackoutRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, max_length=255)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('message_contains_word', models.CharField(blank=True, max_length=255)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
    ]
