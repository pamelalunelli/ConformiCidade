import json
import os
import time
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .forms import CSVUploadForm
from .models import *
from .serializers import CustomUserSerializer
from django.http import HttpResponse
from django.apps import apps
from django.db import connection
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
import base64
from django.template.loader import render_to_string
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import re
from api.models import CustomUser
from django.core.files.base import ContentFile

CustomUser = get_user_model()

'''def detectDelimiter(csvFile: TextIO) -> str:
    dialect = csv.Sniffer().sniff(csvFile.read(1024))
    return dialect.delimiter'''


#@login_required
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
@csrf_exempt
def uploadFile(request):

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                try:
                    iduser_id = CustomUser.objects.get(username=request.user).id
                except CustomUser.DoesNotExist:
                    # Lidar com o caso em que o usuário não é encontrado
                    iduser_id = None

                arquivo_csv = form.cleaned_data['csv_arq']
                nome_arquivo = arquivo_csv.name

                arquivo_formatado = arquivo_csv.read().decode('utf-8').splitlines()
                
                cabecalho = arquivo_formatado[0]

                if cabecalho.startswith('\ufeff'):
                    cabecalho = cabecalho[1:]

                campos = cabecalho.split(',')
                campos = [cleaningColumnName(campo) for campo in campos]

                dados_csv = []

                if len(arquivo_formatado) == 1:
                    dados_com_cabecalho = [dict(zip(campos, [''] * len(campos)))]
                else:
                    for linha in arquivo_formatado[1:]:
                        dados_linha = linha.split(',')
                        dados_csv.append(dados_linha)

                    dados_com_cabecalho = [dict(zip(campos, linha)) for linha in dados_csv]

                tabela_nome = f"input_{int(time.time())}"

                #modelo_dinamico = ModeloDinamico.objects.create(nome=nome_arquivo, iduser=user)
                modelo_dinamico = ModeloDinamico.objects.create(nome=nome_arquivo)
                id = modelo_dinamico.id

                # Convertendo os dados em JSON
                dados_json = json.dumps(dados_com_cabecalho)

                # Salvando os dados JSON no objeto modelo_dinamico
                modelo_dinamico.dataJSON = dados_json

                # Salvando os dados CSV no objeto modelo_dinamico
                modelo_dinamico.dataCSV = '\n'.join(arquivo_formatado)

                modelo_dinamico.iduser = iduser_id
                modelo_dinamico.matchingTableName = "matching_" + tabela_nome.replace('"', '')
                modelo_dinamico.save()

                response_data = {'id': id, 'fields': campos, 'tableName': tabela_nome}
                print("response_data")
                print(response_data)
                print(f"CSV processado com sucesso! ID: {id}")

                return JsonResponse(response_data)
            except Exception as e:
                print(f"Erro ao processar: {e}")
                return JsonResponse({'error': 'Erro interno ao processar a solicitação'}, status=500)
        else:
            print("Formulário inválido:", form.errors)
            return JsonResponse({'error': 'Formulário inválido'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
#def createTable(tabela_nome, campos_renomeados, dados_csv, iduserdata):
def createTable(tabela_nome, campos_renomeados, dados_csv):
    with connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {tabela_nome}")

        '''sql_cria_tabela = f"""
        CREATE TABLE {tabela_nome} (
            id_pk serial PRIMARY KEY,
            iduserdata integer,
            {', '.join([cleaningColumnName(campo) + ' VARCHAR(255)' for campo in campos_renomeados])}
        )
        """'''

        sql_cria_tabela = f"""
        CREATE TABLE {tabela_nome} (
            id_pk serial PRIMARY KEY,
            {', '.join([cleaningColumnName(campo) + ' VARCHAR(255)' for campo in campos_renomeados])}
        )
        """

        print("SQL Criar Tabela:", sql_cria_tabela)
        cursor.execute(sql_cria_tabela)

        '''sql_insere_tabela = f"""
        INSERT INTO {tabela_nome} (iduserdata, {', '.join(campos_renomeados)})
        VALUES (%s, {', '.join(['%s' for _ in campos_renomeados])})
        """'''
        
        sql_insere_tabela = f"""
        INSERT INTO {tabela_nome} ({', '.join(campos_renomeados)})
        VALUES (%s, {', '.join(['%s' for _ in campos_renomeados])})"""

        values = []
        for linha in dados_csv:
            #linha_valores = [iduserdata] + linha
            linha_valores = linha
            values.append(linha_valores)

        print("Valores a serem inseridos:", values)
        cursor.executemany(sql_insere_tabela, values)

@csrf_exempt
def cleaningColumnName(columnName):
    # Substituir caracteres não alfanuméricos por underscores
    return re.sub(r'\W|^(?=\d)', '_', columnName)

@csrf_exempt
def userData(request, id):

    modelo_dinamico = get_object_or_404(ModeloDinamico, id=id)

    try:
        objectsJson = json.loads(modelo_dinamico.data)
    except json.JSONDecodeError:
        objectsJson = []

    if objectsJson and isinstance(objectsJson, list):
        first_object = objectsJson[0] if objectsJson else {}
        fieldsName = list(first_object.keys())
    else:
        fieldsName = []

    return JsonResponse(fieldsName, safe=False)

@csrf_exempt
def defaultDataTable(request):

    excludedTables = ['FieldMatching', 'ModeloDinamico', 'CustomUser', 'AdminUser']
    models = apps.get_app_config('api').get_models()
    tables = []
    for model in models:
        if model._meta.app_label == 'api' and not model._meta.abstract and model._meta.object_name not in excludedTables:
            modelName = model._meta.object_name
            fields = [field.name for field in model._meta.get_fields() if field.concrete and field.name != 'id']
            table = {
                'name': modelName,
                'fields': fields,
            }
            tables.append(table)
    return JsonResponse(tables, safe=False)

@api_view(['POST'])
@csrf_exempt
def autosaveForm(request):
    if request.method == 'POST':
        try:

            data = json.loads(request.body)
            idDinamicModel = data.pop('userDataId', None)
            userId = CustomUser.objects.get(username=request.user).id

            with connection.cursor() as cursor:
                # Consulta para obter o nome da tabela
                sql = """
                    SELECT api_modelodinamico."matchingTableName"
                    FROM api_modelodinamico 
                    WHERE id = %s AND iduser = %s
                """
                cursor.execute(sql, (idDinamicModel, userId))

                #print(sql)
                matchingTableName = cursor.fetchone()[0]


            user_choices = {}  
            for tableNameTest, fieldsData in data.items():
                for referenceFieldTest, inputFieldTest in fieldsData.items():
                    if inputFieldTest.strip():
                        existing_field_matching = FieldMatching.objects.filter(
                            referenceField=referenceFieldTest,
                            tableName=tableNameTest,
                            iduserdata=idDinamicModel,
                            matchingTableName=matchingTableName
                        ).first()
                        if existing_field_matching:
                            existing_field_matching.inputField = inputFieldTest
                            existing_field_matching.save()
                        else:
                            FieldMatching.objects.create(
                                inputField=inputFieldTest,
                                referenceField=referenceFieldTest,
                                tableName=tableNameTest,
                                iduserdata=idDinamicModel,
                                matchingTableName=matchingTableName
                            )
                        user_choices.setdefault(tableNameTest, {})[referenceFieldTest] = inputFieldTest
            
            # Opcional: Você pode adicionar uma resposta personalizada aqui se desejar
            
            return HttpResponse("Dados salvos automaticamente", status=200)

        except Exception as e:
            return HttpResponse("Ocorreu um erro ao processar os dados: " + str(e), status=500)

@api_view(['POST'])
@csrf_exempt
def identifyingAutosavedFields(request):

    data = json.loads(request.body)
    userId = CustomUser.objects.get(username=request.user).id
    idDinamicModel = data.pop('userDataId', None)

    with connection.cursor() as cursor:
        sql = """
        SELECT af."inputField", af."referenceField"
        FROM api_fieldmatching AS af
        WHERE iduserdata = %s
        AND af."inputField" <> ''
        AND af."referenceField" IS NOT NULL
        """
        cursor.execute(sql, (idDinamicModel,))
        autosavedFields = cursor.fetchall()

        sql = """
        SELECT DISTINCT af."matchingTableName"
        FROM api_fieldmatching AS af
        WHERE iduserdata = %s
        """
        cursor.execute(sql, (idDinamicModel,))
        matchingTableName = cursor.fetchone()[0]

        if autosavedFields:
            conditions = ' OR '.join([f"(inputField = %s AND referenceField = %s)" for field in autosavedFields])
            values = [(field[0], field[1]) for field in autosavedFields]

            sql_update = f"""
            UPDATE {matchingTableName} 
            SET userChoice = TRUE
            WHERE {conditions}
            """
            
            cursor.execute(sql_update, [item for sublist in values for item in sublist])

        transaction.commit()

    return Response({"message": "Campos salvos automaticamente"})

@api_view(['POST'])
@csrf_exempt
def processForm(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            idDinamicModel = data.pop('userDataId', None)
            userId = CustomUser.objects.get(username=request.user).id
            #print("o userid é: ", userId)

            with connection.cursor() as cursor:
                # Consulta para obter o nome da tabela
                sql = """
                    SELECT api_modelodinamico."matchingTableName"
                    FROM api_modelodinamico 
                    WHERE id = %s AND iduser = %s
                """
                cursor.execute(sql, (idDinamicModel, userId))

                #print(sql)
                matchingTableName = cursor.fetchone()[0]


            for tableNameTest, fieldsData in data.items():
                for referenceFieldTest, inputFieldTest in fieldsData.items():
                    field_matching, created = FieldMatching.objects.get_or_create(
                        inputField=inputFieldTest,
                        referenceField=referenceFieldTest,
                        tableName=tableNameTest,
                        iduserdata=idDinamicModel,
                        matchingTableName=matchingTableName
                    )
                    if not created:
                        field_matching.inputField = inputFieldTest
                        field_matching.save()
            
            response = generateReport(idDinamicModel)
            pdf_content_base64 = base64.b64encode(response.content).decode('utf-8')

            pdf_name = f'{matchingTableName}.pdf'
            model = ModeloDinamico.objects.get(iduser=userId, id=idDinamicModel)
            
            model.pdfFile.save(pdf_name, ContentFile(pdf_content_base64), save=True)

            return HttpResponse(render_to_string('open_pdf_window.html', {'pdf_content_base64': pdf_content_base64}), status=200)

        except Exception as e:
            return HttpResponse("Ocorreu um erro ao processar os dados: " + str(e), status=500)

def generateReport(iduserdata):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    fieldMatchings = FieldMatching.objects.filter(iduserdata=iduserdata)

    tableData = {}
    tableConformity = {}

    for fieldMatching in fieldMatchings:
        if fieldMatching.tableName not in tableData:
            tableData[fieldMatching.tableName] = []
            tableConformity[fieldMatching.tableName] = {'conform': 0, 'nonconform': 0}

        tableData[fieldMatching.tableName].append(fieldMatching)
        if fieldMatching.referenceField and fieldMatching.inputField:
            tableConformity[fieldMatching.tableName]['conform'] += 1
        else:
            tableConformity[fieldMatching.tableName]['nonconform'] += 1

    buffer = response

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Definindo estilos
    sampleStyles = getSampleStyleSheet()
    boldStyle = ParagraphStyle(name='Bold', parent=sampleStyles["Normal"])
    boldStyle.fontName = 'Helvetica-Bold'
    sampleStyles.add(boldStyle)

    # Adicionando títulos
    elements.append(Paragraph("Relatório de Conformidade", sampleStyles["Title"]))
    elements.append(Paragraph("Comparação entre Modelo de", sampleStyles["Heading3"]))
    elements.append(Paragraph("Referência e Arquivo de entrada", sampleStyles["Heading3"]))

    for tableName, matches in tableData.items():
        elements.append(Paragraph(f'<b>{tableName}</b>', sampleStyles["Heading2"]))

        data = [['Campo de Referência', 'Campo de Entrada', 'Conformidade']]
        for match in matches:
            referenceField = match.referenceField
            inputField = match.inputField
            conformity = 'Conforme' if referenceField and inputField else 'Não Conforme'
            data.append([referenceField, inputField, conformity])

        table = Table(data, colWidths=[180, 180, 90], hAlign='LEFT')
        table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                                   ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                                   ('LINEABOVE', (0, 1), (-1, -1), 1, colors.black),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(table)

        totalFields = len(matches)
        totalConformFields = tableConformity[tableName]['conform']
        conformityPercentage = (totalConformFields / totalFields) * 100
        conformityPercentage = round(conformityPercentage, 2)

        elements.append(Paragraph(f'Percentual de conformidade: {conformityPercentage}%', sampleStyles["Normal"]))

    overallConformityPercentage = (sum(tc['conform'] for tc in tableConformity.values()) / sum(len(td) for td in tableData.values())) * 100
    overallConformityPercentage = round(overallConformityPercentage, 2)
    elements.append(Paragraph(f'<b>Percentual geral de conformidade: {overallConformityPercentage}%</b>', sampleStyles["Bold"]))

    elements.append(Paragraph("<br/><br/>", sampleStyles["Normal"]))

    doc.build(elements)

    pdfContent = buffer.getvalue()
    buffer.close()

    response.write(pdfContent)

    return response

@api_view(['GET'])
@csrf_exempt 
@permission_classes([IsAuthenticated])
def unfinishedMatching(request):
    try:
        # Obtém o ID do usuário autenticado
        userId = CustomUser.objects.get(username=request.user).id
        
        print("User id é:", userId)

        # Filtra os modelos dinâmicos associados ao ID do usuário
        userModels = ModeloDinamico.objects.filter(iduser=userId, isConcluded=False).values()
        return JsonResponse(list(userModels), safe=False)
    except CustomUser.DoesNotExist:
        # Se o usuário não existir, retorna uma lista vazia
        return JsonResponse([], safe=False)

@api_view(['POST'])
@csrf_exempt 
def isConcluded(request):
    if request.method == 'POST':
        # Obtém os dados do corpo da requisição no formato JSON
        data = request.data
        userDataId = data.get('userDataId')
        isConcluded = data.get('isConcluded')
        
        try:
            modelo_dinamico = ModeloDinamico.objects.get(id=userDataId)
            modelo_dinamico.isConcluded = isConcluded
            modelo_dinamico.save()
            
            return JsonResponse({'message': 'Dados atualizados com sucesso'}, status=200)
        except ModeloDinamico.DoesNotExist:
            return JsonResponse({'error': 'Objeto não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

@api_view(['GET'])
@csrf_exempt 
@permission_classes([IsAuthenticated])
def userHistory(request):
    try:
        # Obtém o ID do usuário autenticado
        userId = CustomUser.objects.get(username=request.user).id
        # Filtra os modelos dinâmicos associados ao ID do usuário
        userModels = ModeloDinamico.objects.filter(iduser=userId, isConcluded=True).values()
        # Retorna os modelos dinâmicos como uma resposta JSON
        return JsonResponse(list(userModels), safe=False)
    except CustomUser.DoesNotExist:
        # Se o usuário não existir, retorna uma lista vazia
        return JsonResponse([], safe=False)


@api_view(['GET'])
def downloadPdf(request, pdf_id):
    try:
        # Recupere o objeto ModeloDinamico pelo ID
        model = get_object_or_404(ModeloDinamico, id=pdf_id)

        # Nome completo do arquivo
        file_name = os.path.basename(model.pdfFile.path)

        # Abra o arquivo PDF e leia o conteúdo
        with open(model.pdfFile.path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    except FileNotFoundError:
        return HttpResponse("Arquivo não encontrado", status=404)

@csrf_exempt 
@require_http_methods(["DELETE"])
def userHistoryDelete(request, id):
    try:
        ModeloDinamico.objects.get(pk=id).delete()
        return JsonResponse({'mensagem': 'Objeto excluído com sucesso.'})
    except ModeloDinamico.DoesNotExist:
        return JsonResponse({'erro': 'O objeto não foi encontrado.'}, status=404)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["PATCH"])
def userHistoryEdit(request, id):
    try:
        object = ModeloDinamico.objects.get(pk=id)
        data = json.loads(request.body.decode('utf-8'))
        newName = data.get('nome', None)
        
        if newName is not None:
            object.nome = newName
            object.save()

            return JsonResponse({'mensagem': 'Campo editado com sucesso.'})
        else:
            return JsonResponse({'erro': 'O novo nome não foi fornecido.'}, status=400)

    except ModeloDinamico.DoesNotExist:
        return JsonResponse({'erro': 'O objeto não foi encontrado.'}, status=404)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        user_info = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
        token, created = Token.objects.get_or_create(user=user)
        print("esse é o token_key", token.key)
        print("esse é o user_info", user_info)

        # Crie um objeto HttpRequest apropriado
        #django_request = HttpRequest()
        #django_request.method = 'POST'
        #django_request.POST = request.data

        # Chame a função login() passando o objeto HttpRequest
        #login(django_request, user)

        return Response({'token': token.key, 'user_info': user_info}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    
class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CheckAvailabilityView(CreateAPIView):
    def get(self, request):
        emails = CustomUser.objects.values_list('email', flat=True)
        usernames = CustomUser.objects.values_list('username', flat=True)

        return Response({'emails': emails, 'usernames': usernames}, status=status.HTTP_200_OK)
    
def minha_view(request):
    #print("Usuário autenticado:", request.user.is_authenticated)
    if request.user.is_authenticated:
        # Usuário autenticado, faça o que precisar aqui
        return JsonResponse({'message': 'Usuário está logado'})
    else:
        # Usuário não autenticado, pode retornar uma resposta de erro ou redirecionar para a página de login
        return JsonResponse({'error': 'Usuário não está logado'}, status=401)
