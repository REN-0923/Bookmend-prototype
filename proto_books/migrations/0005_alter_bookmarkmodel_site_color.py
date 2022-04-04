# Generated by Django 4.0.3 on 2022-04-02 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proto_books', '0004_alter_bookmarkmodel_site_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmarkmodel',
            name='site_color',
            field=models.IntegerField(choices=[(1, '🟥red'), (2, '🟦blue'), (3, '🟩green'), (4, '🟨yellow'), (5, '🟧orange'), (6, '⬛black'), (7, '⬜gray'), (8, '🟪purple')], default=2),
        ),
    ]
