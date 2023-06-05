from django.urls import path
from django.contrib import admin
from condominio.views import listacondominio
# from . import views


# app_name = 'condominio'

urlpatterns = [
    path('listacondominio/<int:id>', listacondominio, name='listacondominio'),




]
