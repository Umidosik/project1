# Generated by Django 5.1.3 on 2024-12-14 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0005_alter_tour_average_rating_delete_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='images/')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='tour',
            name='image',
        ),
        migrations.AddField(
            model_name='tour',
            name='images',
            field=models.ManyToManyField(related_name='tours', to='tours.image'),
        ),
    ]