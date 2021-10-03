# Generated by Django 3.2.7 on 2021-09-16 14:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='favorite',
            field=models.ManyToManyField(related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]