# Generated by Django 2.2.6 on 2019-12-02 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20191027_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_title', models.CharField(max_length=30)),
                ('restaurant_name', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=50, unique=True)),
                ('date_written', models.DateTimeField(verbose_name='date written')),
                ('review_text', models.CharField(max_length=250)),
                ('star_rating', models.DecimalField(decimal_places=1, max_digits=2)),
            ],
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]
