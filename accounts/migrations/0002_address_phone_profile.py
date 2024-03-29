# Generated by Django 3.0.5 on 2020-05-05 02:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import localflavor.br.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', localflavor.br.models.BRCPFField(default=None, max_length=14, verbose_name='CPF')),
                ('rg', models.CharField(default=None, max_length=9, verbose_name='RG')),
                ('birthday', models.DateField(default=None, verbose_name='Data de Nascimento')),
                ('civil_status', models.IntegerField(choices=[(0, 'Solteiro (a)'), (1, 'Casado (a)'), (2, 'Divorciado (a)'), (3, 'Viúvo (a)'), (4, 'Outro')], default=0, verbose_name='Estado Civil')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ddi', models.CharField(default=None, max_length=3, null=True, verbose_name='DDI')),
                ('ddd', models.CharField(default=None, max_length=3, null=True, verbose_name='DDD')),
                ('number', models.CharField(default=None, max_length=9, null=True, verbose_name='Número')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone', to='accounts.Profile', verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Telefone',
                'verbose_name_plural': 'Telefones',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postalcode', localflavor.br.models.BRPostalCodeField(default=None, max_length=9, null=True, verbose_name='CEP')),
                ('street_name', models.CharField(default=None, max_length=255, null=True, verbose_name='Endereço')),
                ('street_number', models.CharField(default=None, max_length=10, null=True, verbose_name='Número')),
                ('complement', models.CharField(default=None, max_length=100, null=True, verbose_name='Complemento')),
                ('neighborhood', models.CharField(default=None, max_length=100, null=True, verbose_name='Bairro')),
                ('city', models.CharField(default=None, max_length=100, null=True, verbose_name='Cidade')),
                ('state', localflavor.br.models.BRStateField(default=None, max_length=2, null=True, verbose_name='Estado')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='accounts.Profile', verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Endereço',
                'verbose_name_plural': 'Endereços',
            },
        ),
    ]
