from django.db import models, connection
from django.db.models import Avg, Count, Min, Sum
from conta.models import Contas
from tipocalculo.models import TipoCalculo
from cadastro.models import Cadastro
from condominio.models import Morador, Bloco
from django.utils.safestring import mark_safe
from utils import utils
from django.shortcuts import render


class Calculos(models.Model):
    id_calculos = models.AutoField(primary_key=True)
    id_morador = models.ForeignKey(
        Morador, models.DO_NOTHING, db_column='id_morador')


#    models.IntegerField()
    id_contas = models.ForeignKey(
        Contas, models.DO_NOTHING, db_column='id_contas', related_name='id_contas')
    valor = models.FloatField()
    publica = models.BooleanField(default=True)
    dt_lancamento = models.DateTimeField()
    mesano = models.CharField(max_length=6)

    def get_formatvalorCal(self):
        return f'{self.valor:.2f}'.replace('.', ',')
    get_formatvalorCal.short_description = 'Valor'

    def get_nome_moradorCal(self):
        return '%s' % (self.id_morador.id_inquilino).nome
    get_nome_moradorCal.short_description = 'Morador'

   # @property
    def get_apto_salaCal(self):
        return '%s' % (self.id_morador.apto_sala)
    get_apto_salaCal.short_description = 'Apto/sala'

    def get_contascalculo(self):
        return '%s' % (self.id_contas.nome)
    get_contascalculo.short_description = 'Contas'

    def get_formata_mesano_calculo(self):
        return utils.formata_mesano(self.mesano)
    get_formata_mesano_calculo.short_description = 'MES/ANO'

    def __str__(self) -> str:
        return self.mesano

    class Meta:
        managed = False
        db_table = 'calculos'
        verbose_name = 'Calculo'
        verbose_name_plural = 'Calculos'
        ordering = [
            'mesano', 'id_morador', 'id_contas'
        ]


class Leituras(models.Model):
    id_leituras = models.AutoField(primary_key=True)
    mesano = models.CharField(max_length=6, verbose_name='MES/ANO')
    id_morador = models.ForeignKey(
        Morador, models.DO_NOTHING, db_column='id_morador')
    id_contas = models.ForeignKey(
        Contas, models.DO_NOTHING, db_column='id_contas')
    dt_leitura = models.DateField()
    valor_m3 = models.FloatField()
    leitura_inicial = models.FloatField()
    leitura_final = models.FloatField()

    def get_formatvalorm3(self):
        return f'{self.valor_m3:.2f}'.replace('.', ',')
    get_formatvalorm3.short_description = 'Valor m3'

    def get_contasleitura(self):
        return '%s' % (self.id_contas.nome)
    get_contasleitura.short_description = 'Contas'

    def get_nome_moradorLei(self):
        return '%s' % (self.id_morador.id_inquilino).nome
    get_nome_moradorLei.short_description = 'Morador'

   # @property
    def get_apto_salaLei(self):
        return '%s' % (self.id_morador.apto_sala)
    get_apto_salaLei.short_description = 'Apto/sala'

    def get_formata_mesano_leitura(self):
        return utils.formata_mesano(self.mesano)
    get_formata_mesano_leitura.short_description = 'MES/ANO'

    def __str__(self) -> str:
        return self.mesano

    class Meta:
        managed = False
        db_table = 'leituras'
        verbose_name = 'Leitura'
        verbose_name_plural = 'Leituras'


class Movimento(models.Model):
    id_movimento = models.AutoField(primary_key=True)
    mesano = models.CharField(max_length=6)
    id_bloco = models.ForeignKey(
        Bloco, models.DO_NOTHING, db_column='id_bloco')
    id_contas = models.ForeignKey(
        Contas, models.DO_NOTHING, db_column='id_contas')
    valor = models.FloatField()
    id_tipo_calculo = models.ForeignKey(
        TipoCalculo, models.DO_NOTHING, db_column='id_tipo_calculo')
    dt_lancamento = models.DateTimeField()

    def get_contasmovimento(self):
        return '%s' % (self.id_contas.nome)
    get_contasmovimento.short_description = 'Contas'

    def get_tipo_calculomov(self):
        return '%s' % (self.id_tipo_calculo.descricao)
    get_tipo_calculomov.short_description = 'Tipo Conta'

    def get_formatValorMov(self):
        return f'{self.valor:.2f}'.replace('.', ',')
    get_formatValorMov.short_description = 'Valor'

    def get_formata_mesano_movimento(self):
        return utils.formata_mesano(self.mesano)
    get_formata_mesano_movimento.short_description = 'MES/ANO'

    def __str__(self) -> str:
        return self.mesano

    class Meta:
        managed = False
        db_table = 'movimento'
        unique_together = (('mesano', 'id_contas'),)
        verbose_name = 'Movimento'
        verbose_name_plural = 'Movimentos'
