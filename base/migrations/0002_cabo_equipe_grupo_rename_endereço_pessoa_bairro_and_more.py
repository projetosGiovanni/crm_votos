# Generated by Django 4.0.5 on 2022-07-16 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cabo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Equipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupo', models.CharField(max_length=200)),
                ('rgb', models.CharField(blank=True, max_length=9, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='pessoa',
            old_name='endereço',
            new_name='bairro',
        ),
        migrations.AddField(
            model_name='pessoa',
            name='cep',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='cidade',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='logradouro',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='nascimento',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='telefone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='Voto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cabo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.cabo')),
                ('eleitor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.pessoa')),
            ],
        ),
        migrations.CreateModel(
            name='Líder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.equipe')),
                ('líder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.pessoa')),
            ],
        ),
        migrations.AddField(
            model_name='equipe',
            name='coordenador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.pessoa'),
        ),
        migrations.AddField(
            model_name='equipe',
            name='grupo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.grupo'),
        ),
        migrations.AddField(
            model_name='cabo',
            name='cabo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.pessoa'),
        ),
        migrations.AddField(
            model_name='cabo',
            name='líder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.líder'),
        ),
    ]
