import json
from django.apps import apps
from django.db import connection
from django.http import HttpResponse, JsonResponse
import textdistance as td
import pandas as pd

from django.http import JsonResponse

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
                    inputField VARCHAR(255),
                    referenceField VARCHAR(255),
                    tableName VARCHAR(255),
                    editBased_hamming FLOAT DEFAULT 0.0,
                    editBased_mlipns FLOAT DEFAULT 0.0,
                    editBased_levenshtein FLOAT DEFAULT 0.0,
                    editBased_dameraulevenshtein FLOAT DEFAULT 0.0,
                    editBased_jarowinkler FLOAT DEFAULT 0.0,
                    editBased_strcmp95 FLOAT DEFAULT 0.0,
                    editBased_needlemanwunsch FLOAT DEFAULT 0.0,
                    editBased_gotoh FLOAT DEFAULT 0.0,
                    editBased_smithwaterman FLOAT DEFAULT 0.0,
                    tokenBased_jaccardindex FLOAT DEFAULT 0.0,
                    tokenBased_sørensendicecoefficient FLOAT DEFAULT 0.0,
                    tokenBased_tverskyindex FLOAT DEFAULT 0.0,
                    tokenBased_overlapcoefficient FLOAT DEFAULT 0.0,
                    tokenBased_cosinesimilarity FLOAT DEFAULT 0.0,
                    tokenBased_mongeelkan FLOAT DEFAULT 0.0,
                    tokenBased_bagdistance FLOAT DEFAULT 0.0,
                    sequenceBased_lcsseq FLOAT DEFAULT 0.0,
                    sequenceBased_lcsstr FLOAT DEFAULT 0.0,
                    sequenceBased_ratcliffobershelpsimilarity FLOAT DEFAULT 0.0,
                    compressionBased_arithmeticcoding FLOAT DEFAULT 0.0,
                    compressionBased_rle FLOAT DEFAULT 0.0,
                    compressionBased_bwtrle FLOAT DEFAULT 0.0,
                    compressionBased_squareroot FLOAT DEFAULT 0.0,
                    compressionBased_entropy FLOAT DEFAULT 0.0,
                    compressionBased_bz2 FLOAT DEFAULT 0.0,
                    compressionBased_lzma FLOAT DEFAULT 0.0,
                    compressionBased_zlib FLOAT DEFAULT 0.0,
                    phonetic_mra FLOAT DEFAULT 0.0,
                    phonetic_editex FLOAT DEFAULT 0.0,
                    simple_prefix FLOAT DEFAULT 0.0,
                    simple_postfix FLOAT DEFAULT 0.0,
                    simple_length FLOAT DEFAULT 0.0,
                    simple_identity FLOAT DEFAULT 0.0,
                    simple_matrix FLOAT DEFAULT 0.0,
                    generalindex FLOAT DEFAULT 0.0
                )
                """
                cursor.execute(createTableQuery)

            return HttpResponse(tableName, content_type='text/plain')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

def populateMatchingFields(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            matchingTableName = request_data.get('matchingTableName', {}).get('data', '')
            fieldsCSV = request_data.get('fieldsCSV', [])

            referenceFields = getReferenceFields()

            with connection.cursor() as cursor:
                for inputField in fieldsCSV:
                    for referenceField in referenceFields:
                        try:
                            cursor.execute(f"""
                                INSERT INTO {matchingTableName} (inputField, referenceField, tableName)
                                VALUES (%s, %s, %s)
                            """, [inputField, referenceField, matchingTableName])
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
    
def getReferenceFields():
    models = apps.get_models()
    referenceFields = []

    for model in models:
        fields = [field.name for field in model._meta.get_fields() if field.concrete]
        referenceFields.extend(fields)

    return referenceFields

def calculatingSimilarity(tableName):
    
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT inputField, referenceField FROM {tableName}")

        for row in cursor.fetchall():
            inputFieldDBOriginal = row[0]
            referenceFieldDBOriginal = row[1]
            
            inputFieldDB = inputFieldDBOriginal.lower()
            referenceFieldDB = referenceFieldDBOriginal.lower()

            # Cálculo dos índices de similaridade
            editBasedHamming = td.hamming.normalized_similarity(inputFieldDB, referenceFieldDB)
            editBasedMLIPNS = td.mlipns.normalized_similarity(inputFieldDB, referenceFieldDB)
            editBasedLevenshtein = td.levenshtein.normalized_similarity(inputFieldDB, referenceFieldDB)
            editBasedDamerauLevenshtein = td.damerau_levenshtein.normalized_similarity(inputFieldDB, referenceFieldDB)
            editBasedJaroWinkler = td.jaro_winkler.normalized_similarity(inputFieldDB, referenceFieldDB)
            editBasedStrcmp95 = td.strcmp95.normalized_similarity(inputFieldDB, referenceFieldDB)
            editBasedNeedlemanWunsch = td.needleman_wunsch.normalized_similarity(inputFieldDB, referenceFieldDB)
            editBasedGotoh = td.gotoh.normalized_similarity(inputFieldDB, referenceFieldDB)
            editBasedSmithWaterman = td.smith_waterman.normalized_similarity(inputFieldDB, referenceFieldDB)
            tokenBasedJaccardIndex = td.jaccard.normalized_similarity(inputFieldDB, referenceFieldDB)
            tokenBasedSorensenDiceCoefficient = td.sorensen_dice.normalized_similarity(inputFieldDB, referenceFieldDB)
            tokenTverskyIndex = td.tversky.normalized_similarity(inputFieldDB, referenceFieldDB)
            tokenOverlapCoefficient = td.overlap.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenTanimotoDistance = td.tanimoto.normalized_similarity(inputFieldDB, referenceFieldDB)
            tokenCosineSimilarity = td.cosine.normalized_similarity(inputFieldDB, referenceFieldDB)
            tokenMongeElkan = td.monge_elkan.normalized_similarity(inputFieldDB, referenceFieldDB)
            tokenBagDistance = td.bag.normalized_similarity(inputFieldDB, referenceFieldDB)
            sequenceBasedLCSSeq = td.lcsseq.normalized_similarity(inputFieldDB, referenceFieldDB)
            sequenceBasedLCSStr = td.lcsstr.normalized_similarity(inputFieldDB, referenceFieldDB)
            sequenceBasedRatcliffObershelpSimilarity = td.ratcliff_obershelp.normalized_similarity(inputFieldDB, referenceFieldDB)
            compressionBasedArithmeticcoding = td.arith_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            compressionBasedRLE = td.rle_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            compressionBasedBWTRLE = td.bwtrle_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            compressionBasedSquareroot = td.sqrt_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            compressionBasedEntropy = td.entropy_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            compressionBasedBZ2 = td.bz2_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            compressionBasedLZMA = td.lzma_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            compressionBasedZlib = td.zlib_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            phoneticMRA = td.mra.normalized_similarity(inputFieldDB, referenceFieldDB)
            phoneticEditex = td.editex.normalized_similarity(inputFieldDB, referenceFieldDB)
            simplePrefix = td.prefix.normalized_similarity(inputFieldDB, referenceFieldDB)
            simplePostfix = td.postfix.normalized_similarity(inputFieldDB, referenceFieldDB)
            simpleLength = td.length.normalized_similarity(inputFieldDB, referenceFieldDB)
            simpleIdentity = td.identity.normalized_similarity(inputFieldDB, referenceFieldDB)
            simpleMatrix = td.matrix.normalized_similarity(inputFieldDB, referenceFieldDB)
            generalIndex = (editBasedHamming*0.25)  + (editBasedLevenshtein*0.25) + (simplePrefix*0.5)

            cursor.execute(f"""
                            UPDATE {tableName}
                            SET 
                                editBased_hamming = {editBasedHamming}, 
                                editBased_mlipns = {editBasedMLIPNS}, 
                                editBased_levenshtein = {editBasedLevenshtein}, 
                                editBased_dameraulevenshtein = {editBasedDamerauLevenshtein}, 
                                editBased_jarowinkler = {editBasedJaroWinkler}, 
                                editBased_strcmp95 = {editBasedStrcmp95}, 
                                editBased_needlemanwunsch = {editBasedNeedlemanWunsch}, 
                                editBased_gotoh = {editBasedGotoh}, 
                                editBased_smithwaterman = {editBasedSmithWaterman}, 
                                tokenBased_jaccardindex = {tokenBasedJaccardIndex}, 
                                tokenBased_sørensendicecoefficient = {tokenBasedSorensenDiceCoefficient}, 
                                tokenBased_tverskyindex = {tokenTverskyIndex}, 
                                tokenBased_overlapcoefficient = {tokenOverlapCoefficient}, 
                                tokenBased_cosinesimilarity = {tokenCosineSimilarity}, 
                                tokenBased_mongeelkan = {tokenMongeElkan}, 
                                tokenBased_bagdistance = {tokenBagDistance}, 
                                sequenceBased_lcsseq = {sequenceBasedLCSSeq},
                                sequenceBased_lcsstr = {sequenceBasedLCSStr},
                                sequenceBased_ratcliffobershelpsimilarity = {sequenceBasedRatcliffObershelpSimilarity},
                                compressionBased_arithmeticcoding = {compressionBasedArithmeticcoding},
                                compressionBased_rle = {compressionBasedRLE},
                                compressionBased_bwtrle = {compressionBasedBWTRLE},
                                compressionBased_squareroot = {compressionBasedSquareroot},
                                compressionBased_entropy = {compressionBasedEntropy},
                                compressionBased_bz2 = {compressionBasedBZ2},
                                compressionBased_lzma = {compressionBasedLZMA},
                                compressionBased_zlib = {compressionBasedZlib},
                                phonetic_mra = {phoneticMRA},
                                phonetic_editex = {phoneticEditex},
                                simple_prefix = {simplePrefix},
                                simple_postfix = {simplePostfix},
                                simple_length = {simpleLength},
                                simple_identity = {simpleIdentity},
                                simple_matrix = {simpleMatrix},
                                generalindex = {generalIndex}
                            WHERE 
                                inputfield = '{inputFieldDBOriginal}' AND referencefield = '{referenceFieldDBOriginal}'
                        """)

        connection.commit()

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
        combinedReferences = topReferences + sorted(remainingReferences)
        mostProbableReferences[referencefield] = combinedReferences

    return json.dumps(mostProbableReferences, indent=4)
