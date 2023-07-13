# Generated by Django 4.2 on 2023-07-02 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0002_contest_is_rated'),
        ('problems', '0010_alter_attempt_error_test_case'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='contest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='contests.contest', verbose_name='contest'),
        ),
    ]
