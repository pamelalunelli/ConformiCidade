from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class ModeloDinamico(models.Model):
    nome = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.TextField()

class EquipamentoPublico(models.Model):
    id_equipamento = models.AutoField(primary_key=True)
    id_modeloDinamico = models.ForeignKey(ModeloDinamico, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=20, null=True, blank=True)
    tipo = models.CharField(max_length=20, null=True, blank=True)

class Geometria(models.Model):
    id_geom = models.AutoField(primary_key=True)
    id_modeloDinamico = models.ForeignKey(ModeloDinamico, on_delete=models.CASCADE, null=True, blank=True)
    centroide = models.CharField(max_length=20, null=True, blank=True)
    area = models.CharField(max_length=20, null=True, blank=True)

class Proprietario(models.Model):
    id_proprietario = models.AutoField(primary_key=True)
    id_modeloDinamico = models.ForeignKey(ModeloDinamico, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=20, null=True, blank=True)
    data_nasc = models.CharField(max_length=20, null=True, blank=True)
    cpf = models.CharField(max_length=20, null=True, blank=True)

class AdminUser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=90)
    password = models.CharField(max_length=90)

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        verbose_name=_('user permissions'),
        blank=True,
    )
