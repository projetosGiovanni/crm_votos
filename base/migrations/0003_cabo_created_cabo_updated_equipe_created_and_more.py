# Generated by Django 4.0.6 on 2022-07-16 21:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_cabo_equipe_grupo_rename_endereço_pessoa_bairro_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabo',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cabo',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='equipe',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipe',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='grupo',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grupo',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='líder',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='líder',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='voto',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voto',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True, unique=True),
        ),
    ]
