# Generated by Django 4.2.1 on 2023-05-15 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('JesusSaidAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['position']},
        ),
        migrations.CreateModel(
            name='QuoteOfTheDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('verse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JesusSaidAPI.verse')),
            ],
        ),
    ]
