# Generated by Django 5.1.7 on 2025-05-17 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0007_forumcomment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptotoken',
            name='sparkline_7d',
            field=models.JSONField(default=list),
        ),
    ]
