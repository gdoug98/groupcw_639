# Generated by Django 2.2.6 on 2019-11-28 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebuy', '0003_user_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, upload_to='item_pictures'),
        ),
    ]