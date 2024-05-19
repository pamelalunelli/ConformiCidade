import json
from django.apps import apps
from django.db import connection
from django.http import HttpResponse, JsonResponse
import textdistance as td
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.utils.decorators import method_decorator

@csrf_exempt
def createMatchingTable(request):
    if request.method == 'POST':
        try:
            bodyUnicode = request.body.decode('utf-8')
            tableName = bodyUnicode.strip()

            print("o tableName é", tableName)
            with connection.cursor() as cursor:
                
                tableName = "matching_" + tableName.replace('"', '')
                
                cursor.execute(f"DROP TABLE IF EXISTS {tableName}")
                
                createTableQuery = f"""
                CREATE TABLE {tableName} (
                    id serial PRIMARY KEY,
                    iduserdata integer,
                    inputField VARCHAR(255),
                    referenceField VARCHAR(255),
                    modelName VARCHAR(255),
                    --editBased_hamming FLOAT DEFAULT 0.0,
                    --editBased_mlipns FLOAT DEFAULT 0.0,
                    editBased_levenshtein FLOAT DEFAULT 0.0,
                    --editBased_dameraulevenshtein FLOAT DEFAULT 0.0,
                    --editBased_jarowinkler FLOAT DEFAULT 0.0,
                    --editBased_strcmp95 FLOAT DEFAULT 0.0,
                    --editBased_needlemanwunsch FLOAT DEFAULT 0.0,
                    --editBased_gotoh FLOAT DEFAULT 0.0,
                    --editBased_smithwaterman FLOAT DEFAULT 0.0,
                    --tokenBased_jaccardindex FLOAT DEFAULT 0.0,
                    --tokenBased_sørensendicecoefficient FLOAT DEFAULT 0.0,
                    --tokenBased_tverskyindex FLOAT DEFAULT 0.0,
                    --tokenBased_overlapcoefficient FLOAT DEFAULT 0.0,
                    --tokenBased_cosinesimilarity FLOAT DEFAULT 0.0,
                    --tokenBased_mongeelkan FLOAT DEFAULT 0.0,
                    --tokenBased_bagdistance FLOAT DEFAULT 0.0,
                    --sequenceBased_lcsseq FLOAT DEFAULT 0.0,
                    sequenceBased_lcsstr FLOAT DEFAULT 0.0,
                    --sequenceBased_ratcliffobershelpsimilarity FLOAT DEFAULT 0.0,
                    --compressionBased_arithmeticcoding FLOAT DEFAULT 0.0,
                    --compressionBased_rle FLOAT DEFAULT 0.0,
                    --compressionBased_bwtrle FLOAT DEFAULT 0.0,
                    --compressionBased_squareroot FLOAT DEFAULT 0.0,
                    --compressionBased_entropy FLOAT DEFAULT 0.0,
                    --compressionBased_bz2 FLOAT DEFAULT 0.0,
                    --compressionBased_lzma FLOAT DEFAULT 0.0,
                    --compressionBased_zlib FLOAT DEFAULT 0.0,
                    --phonetic_mra FLOAT DEFAULT 0.0,
                    --phonetic_editex FLOAT DEFAULT 0.0,
                    --simple_prefix FLOAT DEFAULT 0.0,
                    --simple_postfix FLOAT DEFAULT 0.0,
                    --simple_length FLOAT DEFAULT 0.0,
                    --simple_identity FLOAT DEFAULT 0.0,
                    --simple_matrix FLOAT DEFAULT 0.0,
                    generalindex FLOAT DEFAULT 0.0,
                    userChoice BOOLEAN DEFAULT FALSE,
                    tableName VARCHAR(255)
                )
                """
                cursor.execute(createTableQuery)

            return HttpResponse(tableName, content_type='text/plain')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def populateMatchingFields(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            matchingTableName = request_data.get('matchingTableName', {}).get('data', '')
            fieldsCSV = request_data.get('fieldsCSV', [])
            userDataId = request_data.get('userDataId', None)

            referenceFieldsByModel = getReferenceFieldsByModel()

            with connection.cursor() as cursor:
                for inputField in fieldsCSV:
                    for model, referenceFields in referenceFieldsByModel.items():
                        for referenceField in referenceFields:
                            try:
                                cursor.execute(f"""
                                    INSERT INTO {matchingTableName} (iduserdata, inputField, referenceField, modelName, tableName)
                                    VALUES (%s, %s, %s, %s, %s)
                                """, [userDataId, inputField, referenceField, model, matchingTableName])
                            except Exception as e:
                                return JsonResponse({'error': str(e)}, status=500)
            
            calculatingSimilarity(matchingTableName)
            topReferencesJSON = findMostProbableReferences(matchingTableName)
            print("--------------------------------------------------------------")
            print(topReferencesJSON)
            print("--------------------------------------------------------------")
            
            return JsonResponse({'topReferencesJSON': topReferencesJSON})
            #return JsonResponse({'message': 'Success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

@csrf_exempt
def getReferenceFieldsByModel():
    referenceFieldsByModel = {}
    excludedModels = ['FieldMatching', 'ModeloDinamico', 'CustomUser', 'AdminUser']
    appModels = apps.get_app_config('api').get_models()
    for model in appModels:
        if model.__name__ not in excludedModels:
            fields = [field.name for field in model._meta.get_fields() if field.concrete and field.name != 'id']
            referenceFieldsByModel[model.__name__] = fields

    return referenceFieldsByModel

@csrf_exempt
def calculatingSimilarity(tableName):
    
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT inputField, referenceField FROM {tableName}")

        for row in cursor.fetchall():
            inputFieldDBOriginal = row[0]
            referenceFieldDBOriginal = row[1]
            
            inputFieldDB = inputFieldDBOriginal.lower()
            referenceFieldDB = referenceFieldDBOriginal.lower()

            # Cálculo dos índices de similaridade
            #editBasedHamming = td.hamming.normalized_similarity(inputFieldDB, referenceFieldDB)
            #editBasedMLIPNS = td.mlipns.normalized_similarity(inputFieldDB, referenceFieldDB)
            editBasedLevenshtein = td.levenshtein.normalized_similarity(inputFieldDB, referenceFieldDB)
            #editBasedDamerauLevenshtein = td.damerau_levenshtein.normalized_similarity(inputFieldDB, referenceFieldDB)
            #editBasedJaroWinkler = td.jaro_winkler.normalized_similarity(inputFieldDB, referenceFieldDB)
            #editBasedStrcmp95 = td.strcmp95.normalized_similarity(inputFieldDB, referenceFieldDB)
            #editBasedNeedlemanWunsch = td.needleman_wunsch.normalized_similarity(inputFieldDB, referenceFieldDB)
            #editBasedGotoh = td.gotoh.normalized_similarity(inputFieldDB, referenceFieldDB)
            #editBasedSmithWaterman = td.smith_waterman.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenBasedJaccardIndex = td.jaccard.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenBasedSorensenDiceCoefficient = td.sorensen_dice.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenTverskyIndex = td.tversky.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenOverlapCoefficient = td.overlap.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenTanimotoDistance = td.tanimoto.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenCosineSimilarity = td.cosine.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenMongeElkan = td.monge_elkan.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenBagDistance = td.bag.normalized_similarity(inputFieldDB, referenceFieldDB)
            #sequenceBasedLCSSeq = td.lcsseq.normalized_similarity(inputFieldDB, referenceFieldDB)
            sequenceBasedLCSStr = td.lcsstr.normalized_similarity(inputFieldDB, referenceFieldDB)
            #sequenceBasedRatcliffObershelpSimilarity = td.ratcliff_obershelp.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedArithmeticcoding = td.arith_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedRLE = td.rle_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedBWTRLE = td.bwtrle_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedSquareroot = td.sqrt_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedEntropy = td.entropy_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedBZ2 = td.bz2_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedLZMA = td.lzma_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedZlib = td.zlib_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #phoneticMRA = td.mra.normalized_similarity(inputFieldDB, referenceFieldDB)
            #phoneticEditex = td.editex.normalized_similarity(inputFieldDB, referenceFieldDB)
            #simplePrefix = td.prefix.normalized_similarity(inputFieldDB, referenceFieldDB)
            #simplePostfix = td.postfix.normalized_similarity(inputFieldDB, referenceFieldDB)
            #simpleLength = td.length.normalized_similarity(inputFieldDB, referenceFieldDB)
            #simpleIdentity = td.identity.normalized_similarity(inputFieldDB, referenceFieldDB)
            #simpleMatrix = td.matrix.normalized_similarity(inputFieldDB, referenceFieldDB)
            #generalIndex = (editBasedHamming*0.25)  + (editBasedLevenshtein*0.25) + (simplePrefix*0.5)
            generalIndex = (editBasedLevenshtein + sequenceBasedLCSStr)/2
            userChoice = False

            cursor.execute(f"""
                            UPDATE {tableName}
                            SET 
                                editBased_levenshtein = {editBasedLevenshtein}, 
                                sequenceBased_lcsstr = {sequenceBasedLCSStr},
                                generalindex = {generalIndex},
                                userChoice = 'False'
                            WHERE 
                                inputfield = '{inputFieldDBOriginal}' AND referencefield = '{referenceFieldDBOriginal}'
                        """)

        connection.commit()

api_view(['POST'])
@csrf_exempt
def retrievingMatchingFields(request):
    if request.method == 'POST':

        request_data = json.loads(request.body)
        matchingTableName = request_data.get('matchingTableName', '')

        try:
            topReferencesJSON = findMostProbableReferences(matchingTableName)
            return JsonResponse({'topReferencesJSON': topReferencesJSON})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

@csrf_exempt
def findMostProbableReferences(tableName, topN=5):
    with connection.cursor() as cursor:
        query = f"""
            SELECT inputfield, referencefield, generalindex 
            FROM {tableName}
        """
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)

    grouped = df.groupby('referencefield')

    mostProbableReferences = {}
    for referencefield, group in grouped:
        topReferences = group.nlargest(topN, 'generalindex')['inputfield'].tolist()
        remainingReferences = group[~group['inputfield'].isin(topReferences)]['inputfield'].tolist()
        combinedReferences = ['SUGESTÃO'] + topReferences + ['ORDEM ALFABÉTICA'] + sorted(remainingReferences)
        mostProbableReferences[referencefield] = combinedReferences

    return json.dumps(mostProbableReferences, indent=4)

    #if tiver pelo menos um campo userChoice verdadeiro:
    #    lógica para o front pegar essas opções que o usuário já escolheu (inputField) e colocar como valor pré-selecionado no select (usando referencefield
    #     e modelName como referencia)
    #    e para os campos que estejam com false (usando referencefield e modelName como referencia), deve manter a ordem calculada aqui no 
    #    início desse método)

api_view(['POST'])
@csrf_exempt
def getUserChoices(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        table_name = data.get('matchingTableName')

        if not table_name:
            return JsonResponse({'error': 'Parameter "matchingTableName" is required'}, status=400)

        with connection.cursor() as cursor:
            query = f"""
            SELECT modelname, referencefield, inputfield
            FROM {table_name}
            WHERE userchoice = True
            """
            cursor.execute(query)
            data = cursor.fetchall()
            userChoices = {}
            for row in data:
                model_name, reference_field, input_field = row
                if model_name not in userChoices:
                    userChoices[model_name] = {}
                userChoices[model_name][reference_field] = input_field

        return JsonResponse(userChoices, safe=False)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


#Populando a tabela de descrição dos campos

'''INSERT INTO public.api_fielddescription
(id, "fieldName", "fieldDescription", "fieldModel", "fieldType")
VALUES
    (1, 'status', 'Status da edificação', 'BR_CaracteristicasEdificacao', 'varchar'),
    (2, 'tipologia', 'Tipologia da edificação', 'BR_CaracteristicasEdificacao', 'varchar'),
    (3, 'elevador', 'Presença de elevador na edificação', 'BR_CaracteristicasEdificacao', 'varchar'),
    (4, 'posicao', 'Posição da edificação', 'BR_CaracteristicasEdificacao', 'varchar'),
    (5, 'conservacao', 'Estado de conservação da edificação', 'BR_CaracteristicasEdificacao', 'varchar'),
    (6, 'orientacao', 'Orientação da edificação', 'BR_CaracteristicasEdificacao', 'varchar'),
    (7, 'esquadria', 'Tipo de esquadria da edificação', 'BR_CaracteristicasEdificacao', 'varchar'),
    (8, 'estrutura', 'Tipo de estrutura da edificação', 'BR_CaracteristicasEdificacao', 'varchar'),
    (9, 'acabamento', 'Tipo de acabamento da edificação', 'BR_CaracteristicasEdificacao', 'varchar'),
    (10, 'utilizacao', 'Utilização principal da edificação', 'BR_CaracteristicasEdificacao', 'varchar'),
    (11, 'utilizacaoSecundaria', 'Utilização secundária da edificação', 'BR_CaracteristicasEdificacao', 'varchar'),
    (12, 'condicao', 'Condição da edificação', 'BR_CaracteristicasEdificacao', 'varchar'),
    (13, 'cobertura', 'Tipo de cobertura da edificação', 'BR_CaracteristicasEdificacao', 'varchar'),
    (14, 'area', 'Área da edificação', 'BR_Edificacao', 'numeric'),
    (15, 'tipoEdificacao', 'Tipo da edificação', 'BR_Edificacao', 'varchar'),
    (16, 'areaTotalTerreno', 'Área total do terreno', 'BR_CaracteristicasTerreno', 'numeric'),
    (17, 'areaTotalTerreno_privativa', 'Área total do terreno privativa', 'BR_CaracteristicasTerreno', 'numeric'),
    (18, 'areaTotalTerreno_comum', 'Área total do terreno comum', 'BR_CaracteristicasTerreno', 'numeric'),
    (19, 'areaTotalConstruida', 'Área total construída', 'BR_CaracteristicasTerreno', 'numeric'),
    (20, 'areaTotalConstruida_privada', 'Área total construída privada', 'BR_CaracteristicasTerreno', 'numeric'),
    (21, 'areaTotalConstruida_comum', 'Área total construída comum', 'BR_CaracteristicasTerreno', 'numeric'),
    (22, 'numCasas', 'Número de casas na edificação', 'BR_CaracteristicasTerreno', 'int'),
    (23, 'numTorres', 'Número de torres na edificação', 'BR_CaracteristicasTerreno', 'int'),
    (24, 'totalUnidadesPrivativas', 'Total de unidades privativas', 'BR_CaracteristicasTerreno', 'int'),
    (25, 'limitacao', 'Limitação do terreno', 'BR_CaracteristicasTerreno', 'varchar'),
    (26, 'topografia', 'Topografia do terreno', 'BR_CaracteristicasTerreno', 'varchar'),
    (27, 'situacao', 'Situação do terreno', 'BR_CaracteristicasTerreno', 'varchar'),
    (28, 'numVagasCobertas', 'Número de vagas cobertas', 'BR_CaracteristicasTerreno', 'int'),
    (29, 'nivelamento', 'Nivelamento do terreno', 'BR_CaracteristicasTerreno', 'varchar'),
    (30, 'energiaEletrica', 'Disponibilidade de energia elétrica', 'BR_Infraestrutura', 'varchar'),
    (31, 'abastecimentoAgua', 'Abastecimento de água', 'BR_Infraestrutura', 'varchar'),
    (32, 'iluminacaoPublica', 'Iluminação pública', 'BR_Infraestrutura', 'varchar'),
    (33, 'esgoto', 'Rede de esgoto', 'BR_Infraestrutura', 'varchar'),
    (34, 'coletaLixo', 'Coleta de lixo', 'BR_Infraestrutura', 'varchar'),
    (35, 'pavimentacao', 'Tipo de pavimentação', 'BR_Infraestrutura', 'varchar'),
    (36, 'telefonia', 'Disponibilidade de telefonia', 'BR_Infraestrutura', 'varchar'),
    (37, 'arborizacao', 'Arborização', 'BR_Infraestrutura', 'varchar'),
    (38, 'passeio', 'Passeio', 'BR_Infraestrutura', 'varchar'),
    (39, 'drenagemPluvial', 'Drenagem pluvial', 'BR_Infraestrutura', 'varchar'),
    (40, 'valorVenal', 'Valor venal do imóvel', 'BR_Tributos', 'numeric'),
    (41, 'IPTU', 'Valor do IPTU', 'BR_Tributos', 'numeric'),
    (42, 'isencaoIPTU', 'Isenção de IPTU', 'BR_Tributos', 'varchar'),
    (43, 'fatorTerreno', 'Fator do terreno', 'BR_Tributos', 'numeric'),
    (44, 'numero', 'Número do endereço', 'BR_EnderecoImovel', 'varchar'),
    (45, 'complemento', 'Complemento do endereço', 'BR_EnderecoImovel', 'varchar'),
    (46, 'bairro', 'Bairro do endereço', 'BR_EnderecoImovel', 'varchar'),
    (47, 'cep', 'CEP do endereço', 'BR_EnderecoImovel', 'varchar'),
    (48, 'tipoLogradouro', 'Tipo de logradouro', 'BR_Logradouro', 'varchar'),
    (49, 'nomeLogradouro', 'Nome do logradouro', 'BR_Logradouro', 'varchar'),
    (50, 'valor', 'Valor da testada', 'BR_Testada', 'numeric'),
    (51, 'inscricaoImobiliaria', 'Inscrição imobiliária', 'BR_ImovelFiscal', 'varchar'),
    (52, 'matriculaImobiliaria', 'Matrícula imobiliária', 'BR_ImovelFiscal', 'varchar'),
    (53, 'descricaoImovel', 'Descrição do imóvel', 'BR_ImovelFiscal', 'varchar'),
    (54, 'dataCriacao', 'Data de criação do registro', 'BR_ImovelFiscal', 'date'),
    (55, 'inscricaoAnterior', 'Inscrição anterior do imóvel', 'BR_ImovelFiscal', 'varchar'),
    (56, 'loteamento', 'Loteamento do imóvel', 'BR_ImovelFiscal', 'varchar'),
    (57, 'distrito', 'Distrito do imóvel', 'BR_ImovelFiscal', 'varchar'),
    (58, 'setor', 'Setor do imóvel', 'BR_ImovelFiscal', 'varchar'),
    (59, 'quadra', 'Quadra do imóvel', 'BR_ImovelFiscal', 'varchar'),
    (60, 'lote', 'Lote do imóvel', 'BR_ImovelFiscal', 'varchar'),
    (61, 'unidade', 'Unidade do imóvel', 'BR_ImovelFiscal', 'varchar'),
    (62, 'endID', 'ID do endereço de correspondência', 'BR_EnderecoCorrespondencia', 'int'),
    (63, 'tipoLogradouro', 'Tipo de logradouro do endereço de correspondência', 'BR_EnderecoCorrespondencia', 'varchar'),
    (64, 'nomeLogradouro', 'Nome do logradouro do endereço de correspondência', 'BR_EnderecoCorrespondencia', 'varchar'),
    (65, 'numero', 'Número do endereço de correspondência', 'BR_EnderecoCorrespondencia', 'varchar'),
    (66, 'complemento', 'Complemento do endereço de correspondência', 'BR_EnderecoCorrespondencia', 'varchar'),
    (67, 'bairro', 'Bairro do endereço de correspondência', 'BR_EnderecoCorrespondencia', 'varchar'),
    (68, 'municipio', 'Município do endereço de correspondência', 'BR_EnderecoCorrespondencia', 'varchar'),
    (69, 'UF', 'UF do endereço de correspondência', 'BR_EnderecoCorrespondencia', 'varchar'),
    (70, 'CEP', 'CEP do endereço de correspondência', 'BR_EnderecoCorrespondencia', 'varchar'),
    (71, 'classificacao', 'Classificação do endereço de correspondência', 'BR_EnderecoCorrespondencia', 'varchar'),
    (72, 'nomeFantasia', 'Nome fantasia da pessoa jurídica', 'BR_PessoaJuridica', 'varchar'),
    (73, 'razao_social', 'Razão social da pessoa jurídica', 'BR_PessoaJuridica', 'varchar'),
    (74, 'estadoCivil', 'Estado civil da pessoa física', 'BR_PessoaFisica', 'varchar'),
    (75, 'nome', 'Nome da pessoa física', 'BR_PessoaFisica', 'varchar'),
    (76, 'idContato', 'ID do contato da pessoa', 'BR_ContatoPessoa', 'int'),
    (77, 'telefone', 'Telefone do contato da pessoa', 'BR_ContatoPessoa', 'varchar'),
    (78, 'celular', 'Celular do contato da pessoa', 'BR_ContatoPessoa', 'varchar'),
    (79, 'email', 'Email do contato da pessoa', 'BR_ContatoPessoa', 'varchar'),
    (80, 'idDoc', 'ID do documento da pessoa', 'BR_DocumentoPessoa', 'int'),
    (81, 'documento', 'Tipo de documento da pessoa', 'BR_DocumentoPessoa', 'varchar'),
    (82, 'numeroDocumento', 'Número do documento da pessoa', 'BR_DocumentoPessoa', 'varchar'),
    (83, 'tipoPessoa', 'Tipo de pessoa', 'BR_Pessoa', 'varchar'),
    (84, 'codContribuinte', 'Código do contribuinte', 'BR_Pessoa', 'varchar');'''