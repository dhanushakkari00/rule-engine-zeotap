# Generated by Django 5.1.2 on 2024-10-24 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rule_engine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='astnode',
            name='operator',
            field=models.CharField(blank=True, choices=[('AND', 'AND'), ('OR', 'OR')], max_length=10, null=True),
        ),
    ]
