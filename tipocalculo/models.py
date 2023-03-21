from django.db import models


class TipoCalculo(models.Model):
    id_tipo_calculo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=5)
    situacao = models.CharField(max_length=1)
    descricao = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.nome

    class Meta:
        managed = False
        db_table = 'tipo_calculo'
        verbose_name = 'Tipo Calculo'
        verbose_name_plural = 'Tipo Calculos'
