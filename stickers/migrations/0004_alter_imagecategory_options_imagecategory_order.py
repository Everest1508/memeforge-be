# Generated by Django 5.0.7 on 2025-05-14 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stickers', '0003_move_images_to_template'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagecategory',
            options={'ordering': ['order'], 'verbose_name_plural': 'Image Categories'},
        ),
        migrations.AddField(
            model_name='imagecategory',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
