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

    appModels = apps.get_app_config('api').get_models()
    for model in appModels:
        fields = [field.name for field in model._meta.get_fields() if field.concrete]
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
                    userChoices[model_name] = []
                userChoices[model_name].append({'reference_field': reference_field, 'input_field': input_field})

        return JsonResponse(userChoices, safe=False)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
