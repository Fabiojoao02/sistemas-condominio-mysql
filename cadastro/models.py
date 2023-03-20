import os
from PIL import Image
from django.db import models
from django.conf import settings
from django.forms import ValidationError

import re
from utils.validacpf import valida_cpf


class Cadastro(models.Model):
    id_cadastro = models.AutoField(primary_key=True)
    cpf_cnpj = models.CharField(unique=True, max_length=14)
    nome = models.CharField(max_length=250)
    endereco = models.CharField(max_length=250)
    bairro = models.CharField(max_length=250)
    cidade = models.CharField(max_length=250)
    estado = models.ForeignKey('Estado', models.DO_NOTHING, db_column='estado')
    cep = models.CharField(max_length=8)
    situacao = models.CharField(max_length=1)
    dt_registro = models.DateTimeField()
    email = models.CharField(max_length=250)
    telefone = models.CharField(max_length=250)
    data_nascimento = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.nome

    class Meta:
        managed = False
        db_table = 'cadastro'
        verbose_name = 'Cadastro'
        verbose_name_plural = 'Cadastros'

    def clean(self):
        error_messages = {}

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'CEP inválido, digite apenas números 8 dígitos'

        if error_messages:
            raise ValidationError(error_messages)


class Estado(models.Model):
    uf = models.CharField(primary_key=True, max_length=2)
    nome = models.CharField(unique=True, max_length=250)

    def __str__(self) -> str:
        return self.nome

    class Meta:
        managed = False
        db_table = 'estado'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
