from django.db import models


class Contas(models.Model):
    id_conta = models.AutoField(primary_key=True)
    nome = models.CharField(unique=True, max_length=250)
    situacao = models.CharField(max_length=1)
    leituras = models.IntegerField()
    # leituras = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.nome

    class Meta:
        managed = False
        db_table = 'contas'
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
