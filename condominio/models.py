# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import os
from PIL import Image
from django.db import models
from django.conf import settings
from django.forms import ValidationError
from cadastro.models import Cadastro, Estado

import re
from utils.validacpf import valida_cpf


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bloco(models.Model):
    id_bloco = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=250)
    situacao = models.CharField(max_length=1)
    id_condominio = models.ForeignKey(
        'Condominio', models.DO_NOTHING, db_column='id_condominio')
    fundo_reserva = models.FloatField()
    taxa_condominio = models.FloatField()
    fracao_ideal = models.FloatField()

    def get_Taxa_condominio(self):
        return f' {self.taxa_condominio:.2f}%'.replace('.', ',')
    get_Taxa_condominio.short_description = 'Tx Condominio'

    def get_Fundo_reserva(self):
        return f' {self.fundo_reserva:.2f}%'.replace('.', ',')
    get_Fundo_reserva.short_description = 'Fundo Reserva'

    def get_Fracao_ideal(self):
        return f' {self.fracao_ideal:.2f}%'.replace('.', ',')
    get_Fracao_ideal.short_description = 'Fração Ideal'

    def __str__(self) -> str:
        return self.nome

    class Meta:
        managed = False
        db_table = 'bloco'
        verbose_name = 'Bloco'
        verbose_name_plural = 'Blocos'


class Condominio(models.Model):
    id_condominio = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=250)
    endereco = models.CharField(max_length=250)
    cidade = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=8)
    estado = models.ForeignKey(
        Estado, models.DO_NOTHING, db_column='estado', related_name='estado')
    foto = models.ImageField(
        upload_to='condominio_imagens', blank=True, null=True)
    mostrar = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'condominio'
        verbose_name = 'Condominio'
        verbose_name_plural = 'Condominios'

    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close
            return
        new_width = round((new_width * original_height) / original_width)
        new_img = img_pil.resize((new_width, new_width), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)

        max_image_size = 800

        if self.Foto:
            self.resize_image(self.Foto, max_image_size)

    def __str__(self) -> str:
        return self.nome


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Morador(models.Model):
    id_morador = models.AutoField(primary_key=True)
    id_inquilino = models.ForeignKey(
        Cadastro, models.DO_NOTHING, db_column='id_inquilino', related_name='id_inquilino')
    id_proprietario = models.ForeignKey(
        Cadastro, models.DO_NOTHING, db_column='id_proprietario', related_name='id_proprietario')
    apto_sala = models.CharField(max_length=80)
    id_bloco = models.ForeignKey(
        Bloco, models.DO_NOTHING, db_column='id_bloco')
    qt_moradores = models.IntegerField()
    situacao = models.CharField(max_length=1)
    responsavel = models.CharField(max_length=1)
    foto = models.ImageField(
        upload_to='morador_imagens', blank=True, null=True)

    def __str__(self) -> str:
        return self.apto_sala

    # @property
    def get_nome_bloco(self):
        return '%s ' % (self.id_bloco.nome)
    get_nome_bloco.short_description = 'Bloco'

    def get_nome_inquilino(self):
        return '%s' % (self.id_inquilino.nome)
    get_nome_inquilino.short_description = 'Inquilino'

    def get_nome_proprietario(self):
        return '%s' % (self.id_proprietario.nome)
    get_nome_proprietario.short_description = 'Proprietário'

    def get_telefone_morador(self):
        return '%s' % (self.id_inquilino.telefone)
    get_telefone_morador.short_description = 'Telefone'

    def get_email_morador(self):
        return '%s' % (self.id_inquilino.email)
    get_email_morador.short_description = 'Telefone'

    def get_cpf_cnpj_morador(self):
       # return f'{self.cpf[0:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:11]}'
        return '%s' % (self.id_inquilino.cpf_cnpj)
    get_cpf_cnpj_morador.short_description = 'CPF/CNPJ'

    class Meta:
        managed = False
        db_table = 'morador'
        verbose_name = 'Morador'
        verbose_name_plural = 'Moradores'
