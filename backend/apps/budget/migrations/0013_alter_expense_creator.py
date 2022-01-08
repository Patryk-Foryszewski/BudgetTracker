# Generated by Django 3.2 on 2022-01-07 18:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budget', '0012_alter_expense_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
