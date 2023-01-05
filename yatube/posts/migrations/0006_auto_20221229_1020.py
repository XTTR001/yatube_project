# Generated by Django 2.2.6 on 2022-12-29 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_group_options_alter_post_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={
                'verbose_name': 'группа',
                'verbose_name_plural': 'группы',
            },
        ),
        migrations.AlterModelOptions(
            name='post',
            options={
                'default_related_name': 'posts',
                'ordering': ('-pub_date',),
                'verbose_name': 'пост',
                'verbose_name_plural': 'посты',
            },
        ),
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='group',
            name='id',
            field=models.AutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name='ID',
            ),
        ),
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=200, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='posts',
                to=settings.AUTH_USER_MODEL,
                verbose_name='автор',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='posts',
                to='posts.Group',
                verbose_name='автор',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.AutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name='ID',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(
                auto_now_add=True, verbose_name='дата публикации'
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(verbose_name='текст'),
        ),
    ]
