from django.db import migrations

def move_images_to_templates(apps, schema_editor):
    Image = apps.get_model('stickers', 'Image')
    Template = apps.get_model('stickers', 'Template')
    ImageCategory = apps.get_model('stickers', 'ImageCategory')

    try:
        meme_template_category = ImageCategory.objects.get(slug='meme-template')
    except ImageCategory.DoesNotExist:
        return

    images = Image.objects.filter(category=meme_template_category)

    templates_to_create = [
        Template(
            name=image.title,
            image=image.image,
            short_description=image.short_description,
        )
        for image in images
    ]

    Template.objects.bulk_create(templates_to_create)
    images.delete()

def move_templates_back_to_images(apps, schema_editor):
    Image = apps.get_model('stickers', 'Image')
    Template = apps.get_model('stickers', 'Template')
    ImageCategory = apps.get_model('stickers', 'ImageCategory')

    meme_template_category, created = ImageCategory.objects.get_or_create(
        slug='meme-template',
        defaults={'name': 'Meme Template'}
    )

    templates = Template.objects.all()

    images_to_create = [
        Image(
            category=meme_template_category,
            title=template.name,
            short_description=template.short_description,
            image=template.image,
        )
        for template in templates
    ]

    Image.objects.bulk_create(images_to_create)
    templates.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('stickers', '0002_template'),
    ]

    operations = [
        migrations.RunPython(move_images_to_templates, move_templates_back_to_images),
    ]
