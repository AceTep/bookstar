# Generated by Django 4.2.7 on 2024-02-15 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_bookcomment_remove_book_comments_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcomment',
            name='rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0),
            preserve_default=False,
        ),
    ]
