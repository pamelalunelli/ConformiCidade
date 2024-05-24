from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework.authtoken.models import Token


class FieldMatching(models.Model):
    #usuer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    iduserdata = models.IntegerField()
    inputField = models.CharField(max_length=255)
    referenceField = models.CharField(max_length=255)
    tableName = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    matchingTableName = models.CharField(max_length=255, null=True)

class ModeloDinamico(models.Model):
    iduser = models.IntegerField(null=True)
    nome = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    dataCSV = models.TextField()
    dataJSON = models.TextField()
    matchingTableName = models.CharField(max_length=255, null=True)
    isConcluded = models.BooleanField(default=False)
    pdfFile = models.FileField(upload_to='pdfs/', null=True)


class FieldDescription (models.Model):
    fieldName = models.CharField(max_length=255, null=True)
    fieldDescription = models.CharField(max_length=5000, null=True)
    fieldModel = models.CharField(max_length=255, null=True)
    fieldType = models.CharField(max_length=255, null=True)

'''class AdminUser(models.Model):
    email = models.CharField(max_length=90)
    password = models.CharField(max_length=90)'''

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        verbose_name=_('user permissions'),
        blank=True,
    )

class BR_CaracteristicasTerreno(models.Model):
    id = models.AutoField(primary_key=True)
    areaTotalTerreno = models.FloatField(null=True, blank=True)
    areaTotalTerreno_privativa = models.FloatField(null=True, blank=True)
    areaTotalTerreno_comum = models.FloatField(null=True, blank=True)
    areaTotalConstruida = models.FloatField(null=True, blank=True)
    areaTotalConstruida_privada = models.FloatField(null=True, blank=True)
    areaTotalConstruida_comum = models.FloatField(null=True, blank=True)
    numCasas = models.IntegerField(null=True, blank=True)
    numTorres = models.IntegerField(null=True, blank=True)
    totalUnidadesPrivativas = models.IntegerField(null=True, blank=True)
    limitacao = models.CharField(max_length=255, null=True, blank=True)
    topografia = models.CharField(max_length=255, null=True, blank=True)
    situacao = models.CharField(max_length=255, null=True, blank=True)
    numVagas = models.IntegerField(null=True, blank=True)
    nivelamento = models.CharField(max_length=255, null=True, blank=True)

class BR_CaracteristicasEdificacao(models.Model):
    id = models.AutoField(primary_key=True)
    area = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    tipologia = models.CharField(max_length=255, null=True, blank=True)
    elevador = models.BooleanField(default=False)  # Assume-se que o padrão é False
    posicao = models.CharField(max_length=255, null=True, blank=True)
    conservacao = models.CharField(max_length=255, null=True, blank=True)
    orientacao = models.CharField(max_length=255, null=True, blank=True)
    esquadria = models.CharField(max_length=255, null=True, blank=True)
    estrutura = models.CharField(max_length=255, null=True, blank=True)
    acabamento = models.CharField(max_length=255, null=True, blank=True)
    utilizacao = models.CharField(max_length=255, null=True, blank=True)
    utilizacaoSecundaria = models.CharField(max_length=255, null=True, blank=True)
    condicao = models.CharField(max_length=255, null=True, blank=True)
    cobertura = models.CharField(max_length=255, null=True, blank=True)

class BR_Infraestrutura(models.Model):
    id = models.AutoField(primary_key=True)
    energiaEletrica = models.BooleanField(default=False)
    abastecimentoAgua = models.BooleanField(default=False)
    iluminacaoPublica = models.BooleanField(default=False)
    esgoto = models.BooleanField(default=False)
    coletaLixo = models.BooleanField(default=False)
    pavimentacao = models.BooleanField(default=False)
    telefonia = models.BooleanField(default=False)
    arborizacao = models.BooleanField(default=False)
    passeio = models.BooleanField(default=False)
    drenagemPluvial = models.BooleanField(default=False)

class BR_Tributo(models.Model):
    id = models.AutoField(primary_key=True)
    valorVenal = models.FloatField(null=True, blank=True)
    IPTU = models.FloatField(null=True, blank=True)
    isencaoIPTU = models.BooleanField(default=False)
    fatorTerreno = models.FloatField(null=True, blank=True)

class BR_TrechoLogradouro(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=255, null=True, blank=True)
    valor = models.FloatField(null=True, blank=True)

class BR_EnderecoImovel(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    complemento = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    cep = models.CharField(max_length=20, null=True, blank=True)

class BR_EnderecoCorrespondencia(models.Model):
    id = models.AutoField(primary_key=True)
    tipoLogradouro = models.CharField(max_length=255, null=True, blank=True)
    nomeLogradouro = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    complemento = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    municipio = models.CharField(max_length=255, null=True, blank=True)
    UF = models.CharField(max_length=2, null=True, blank=True)
    CEP = models.CharField(max_length=20, null=True, blank=True)
    classificacao = models.CharField(max_length=255, null=True, blank=True)

class BR_PessoaJuridica(models.Model):
    id = models.AutoField(primary_key=True)
    nomeFantasia = models.CharField(max_length=255, null=True, blank=True)
    razaoSocial = models.CharField(max_length=255, null=True, blank=True)

class BR_PessoaFisica(models.Model):
    id = models.AutoField(primary_key=True)
    estadoCivil = models.CharField(max_length=255, null=True, blank=True)
    nome = models.CharField(max_length=255, null=True, blank=True)

class BR_ContatoPessoa(models.Model):
    id = models.AutoField(primary_key=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    celular = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

class BR_DocumentoPessoa(models.Model):
    id = models.AutoField(primary_key=True)
    documento = models.CharField(max_length=255, null=True, blank=True)
    numeroDocumento = models.CharField(max_length=255, null=True, blank=True)

class BR_Pessoa(models.Model):
    id = models.AutoField(primary_key=True)
    tipoPessoa = models.CharField(max_length=255, null=True, blank=True)
    codContribuinte = models.CharField(max_length=255, null=True, blank=True)
    papel = models.CharField(max_length=255, null=True, blank=True)
    fk_pessoaFisica = models.OneToOneField(BR_PessoaFisica, on_delete=models.CASCADE, null=True, blank=True)
    fk_pessoaJuridica = models.OneToOneField(BR_PessoaJuridica, on_delete=models.CASCADE, null=True, blank=True)
    fk_contatoPessoa = models.ForeignKey(BR_ContatoPessoa, on_delete=models.CASCADE, null=True, blank=True)
    fk_documentoPessoa = models.ForeignKey(BR_DocumentoPessoa, on_delete=models.CASCADE, null=True, blank=True)

class BR_ImovelFiscal(models.Model):
    id = models.AutoField(primary_key=True)
    inscricaoImobiliaria = models.CharField(max_length=255)
    matriculaImobiliaria = models.CharField(max_length=255)
    descricaoImovel = models.TextField(null=True, blank=True)
    dataCriacao = models.DateField(null=True, blank=True)
    inscricaoAnterior = models.CharField(max_length=255, null=True, blank=True)
    loteamento = models.CharField(max_length=255, null=True, blank=True)
    distrito = models.CharField(max_length=255, null=True, blank=True)
    setor = models.CharField(max_length=255, null=True, blank=True)
    quadra = models.CharField(max_length=255, null=True, blank=True)
    lote = models.CharField(max_length=255, null=True, blank=True)
    unidade = models.CharField(max_length=255, null=True, blank=True)
    testada = models.IntegerField(null=True, blank=True)
    fk_caracteristicasTerreno = models.ForeignKey(BR_CaracteristicasTerreno, on_delete=models.CASCADE, null=True, blank=True)
    fk_caracteristicasEdificacao = models.ForeignKey(BR_CaracteristicasEdificacao, on_delete=models.CASCADE, null=True, blank=True)
    fk_enderecoImovel = models.ForeignKey(BR_EnderecoImovel, on_delete=models.CASCADE, null=True, blank=True)
    fk_infraestrutura = models.ForeignKey(BR_Infraestrutura, on_delete=models.CASCADE, null=True, blank=True)
    fk_tributo = models.ForeignKey(BR_Tributo, on_delete=models.CASCADE, null=True, blank=True)
    fk_trechoLogradouro = models.ForeignKey(BR_TrechoLogradouro, on_delete=models.CASCADE, null=True, blank=True)
    fk_pessoa = models.ManyToManyField(BR_Pessoa)


