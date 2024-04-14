import csv
import json
import time
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .forms import CSVUploadForm
from .models import *
from .serializers import CustomUserSerializer
from .db_utils import createTable
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.apps import apps

CustomUser = get_user_model()

@transaction.atomic
@csrf_exempt
def uploadFile(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                arquivo_csv = form.cleaned_data['csv_arq']
                nome_arquivo = arquivo_csv.name
                arquivo_formatado = arquivo_csv.read().decode('utf-8').splitlines()
                dicionario_csv = csv.DictReader(arquivo_formatado)

                dados_csv = list(dicionario_csv)
                arquivo_csv.seek(0)

                tabela_nome = f"input_{int(time.time())}"
                campos_renomeados = [campo.replace(" ", "_") for campo in dicionario_csv.fieldnames]
                campos = dados_csv[0].keys()

                modelo_dinamico = ModeloDinamico.objects.create(nome=nome_arquivo)
                id = modelo_dinamico.id

                createTable(tabela_nome, campos_renomeados, dados_csv)

                #dados_dinamicos = [{campo: line[campo] for campo in campos} for line in dados_csv]
                #modelo_dinamico.data = json.dumps(dados_dinamicos)
                modelo_dinamico.data = json.dumps(dados_csv)
                modelo_dinamico.save()

                response_data = {'id': id}
                print(f"CSV processado com sucesso! ID: {id}")
                return JsonResponse(response_data)
            except csv.Error as e:
                print(f"Erro ao processar CSV: {e}")
                return JsonResponse({'error': 'Erro ao processar o arquivo CSV'}, status=400)
            except Exception as e:
                print(f"Erro ao processar: {e}")
                return JsonResponse({'error': 'Erro interno ao processar a solicitação'}, status=500)
        else:
            print("Formulário inválido:", form.errors)
            return JsonResponse({'error': 'Formulário inválido'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

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

def defaultDataTable(request):
    #models = [EquipamentoPublico, Geometria, Proprietario]
    models = apps.get_models()

    tables = []

    for model in models:
        modelName = model._meta.object_name
        fields = [field.name for field in model._meta.get_fields() if field.concrete]

        table = {
            'name': modelName,
            'fields': fields,
        }

        tables.append(table)

    return JsonResponse(tables, safe=False)

@csrf_exempt
def processar_formulario(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            for table_name, fields_data in data.items():
                print("primeiro for")
                # Iterar sobre os campos de entrada e campos de referência
                for campo_entrada, campo_referencia in fields_data.items():
                    print("segundo for")
                    # Criar uma instância de CampoMatch com os dados encontrados
                    CampoMatch.objects.create(
                        usuario=request.user,  # Supondo que você tenha um usuário autenticado
                        nome_campo_entrada=campo_entrada,
                        nome_campo_referencia=campo_referencia,
                        modelo_referencia=table_name
                    )

            # Retornar uma resposta de sucesso se tudo der certo
            return HttpResponse("Dados processados com sucesso", status=200)

        except Exception as e:
            # Lidar com exceções, se ocorrerem
            return HttpResponse("Ocorreu um erro ao processar os dados: " + str(e), status=500)
        
            """equipamento_data = data.get('EquipamentoPublico', {})
            geometria_data = data.get('Geometria', {})
            proprietario_data = data.get('Proprietario', {})
            
            print("TESTE1")
            print("este é o equipamento_data", equipamento_data)
            print("este é o geometria_data", geometria_data)
            print("este é o proprietario_data", proprietario_data)

            equipamento_data.pop('id_equipamento', None)
            #equipamento_data['id_modeloDinamico'] = id
            equipamento_data.pop('id_modeloDinamico', None)
            equipamentoPublico = EquipamentoPublico(**equipamento_data)
            geometria_data.pop('id_geom', None)
            #geometria_data['id_modeloDinamico'] = id
            geometria_data.pop('id_modeloDinamico', None)
            geometria = Geometria(**geometria_data)
            proprietario_data.pop('id_proprietario', None)
            #proprietario_data['id_modeloDinamico'] = id
            proprietario_data.pop('id_modeloDinamico', None)
            proprietario = Proprietario(**proprietario_data)

            print("TESTE2")
            print("este é o equipamentoPublico", equipamentoPublico)
            print("este é o geometria", geometria)
            print("este é o proprietario", proprietario)

            equipamentoPublico.save()
            geometria.save()
            proprietario.save()

            print("TESTE3")
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método não permitido'})"""

def showPopulatedRegister (request, id):
    return 0

def generateComplianceReportPdf(request):
    proprietor = Proprietario.objects.latest('id_proprietario')
    equipment = EquipamentoPublico.objects.latest('id_equipamento')
    geom = Geometria.objects.latest('id_geom')
    
    proprietorCompliance = calculateProprietorCompliance(proprietor)
    equipmentCompliance = calculateEquipmentCompliance(equipment)
    geomCompliance = calculateGeomCompliance(geom)
    
    totalFields_proprietor = len(proprietorCompliance)
    totalFields_equipment = len(equipmentCompliance)
    totalFields_geom = len(geomCompliance)
    
    conformantFields_proprietor = sum(1 for c in proprietorCompliance.values() if c == 'Conforme')
    conformantFields_equipment = sum(1 for c in equipmentCompliance.values() if c == 'Conforme')
    conformantFields_geom = sum(1 for c in geomCompliance.values() if c == 'Conforme')
    
    adherencePercentage_proprietor = (conformantFields_proprietor / totalFields_proprietor) * 100 if totalFields_proprietor != 0 else 0
    adherencePercentage_equipment = (conformantFields_equipment / totalFields_equipment) * 100 if totalFields_equipment != 0 else 0
    adherencePercentage_geom = (conformantFields_geom / totalFields_geom) * 100 if totalFields_geom != 0 else 0
    
    totalTables = 3  
    totalAdherencePercentage = (adherencePercentage_proprietor + adherencePercentage_equipment + adherencePercentage_geom) / totalTables
    
    templatePath = 'compliance_report.html'
    context = {
        'proprietor': proprietor,
        'equipment': equipment,
        'geom': geom,
        'proprietorCompliance': proprietorCompliance,
        'equipmentCompliance': equipmentCompliance,
        'geomCompliance': geomCompliance,
        'adherencePercentage_proprietor': adherencePercentage_proprietor,
        'adherencePercentage_equipment': adherencePercentage_equipment,
        'adherencePercentage_geom': adherencePercentage_geom,
        'totalAdherencePercentage': totalAdherencePercentage,
    }
    template = get_template(templatePath)
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="compliance_report.pdf"'
    pisaStatus = pisa.CreatePDF(html, dest=response)
    if pisaStatus.err:
        return HttpResponse('An error occurred while generating the PDF.')
    return response

def calculateProprietorCompliance(proprietor):
    compliance = {}
    for field in Proprietario._meta.get_fields():
        if field.name != 'id_proprietario' and field.name != 'id_modeloDinamico':
            if getattr(proprietor, field.name):
                compliance[field.name] = 'Conforme'
            else:
                compliance[field.name] = 'Não Conforme'
    return compliance

def calculateEquipmentCompliance(equipment):
    compliance = {}
    for field in EquipamentoPublico._meta.get_fields():
        if field.name != 'id_equipamento' and field.name != 'id_modeloDinamico':
            if getattr(equipment, field.name):
                compliance[field.name] = 'Conforme'
            else:
                compliance[field.name] = 'Não Conforme'
    return compliance

def calculateGeomCompliance(geom):
    compliance = {}
    for field in Geometria._meta.get_fields():
        if field.name != 'id_geom' and field.name != 'id_modeloDinamico':
            if getattr(geom, field.name):
                compliance[field.name] = 'Conforme'
            else:
                compliance[field.name] = 'Não Conforme'
    return compliance

def userHistory(request):
    return JsonResponse(list(ModeloDinamico.objects.values()), safe=False)

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