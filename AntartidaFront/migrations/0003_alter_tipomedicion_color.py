# Generated by Django 3.2.9 on 2021-12-21 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AntartidaFront', '0002_auto_20211221_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipomedicion',
            name='color',
            field=models.CharField(blank=True, default='rgba(255, 99, 132, 0.5)', max_length=50, null=True),
        ),
    ]
