from urllib import response
from django.http import JsonResponse
from ConnectCouchdb import *
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ConnectCouchdb.CouchdbCRUD import *
import requests
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from requests.exceptions import ConnectionError
from couchdb import Server

# Connect to CouchDB


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_all_documents_view(request, dbname, type):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "major",type ,settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        documents = get_all_documents(db)
        return Response(documents)
    except ConnectionError:
        try:
            backup_server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "replica",type , settings.COUCHDB_PORT)
            db = get_database(backup_server, dbname)
            documents = get_all_documents(db)
            return Response(documents)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_document_view(request, dbname ,doc_id, type):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "major", type, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        document = get_document(db, doc_id)
        return Response(document)
    
    except ConnectionError:
        try:
            backup_server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "replica",type , settings.COUCHDB_PORT)
            db = get_database(backup_server, dbname)
            document = get_document(db, doc_id)
            return Response(document)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def create_document_view(request, dbname, type):
   try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "major", type, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        document_data = request.data
        print(document_data)
        document = create_document(db, document_data)
        return Response(document)
    
   except ConnectionError:
        try:
            backup_server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "replica",type , settings.COUCHDB_PORT)
            db = get_database(backup_server, dbname)
            document_data = request.data
            document = create_document(db, document_data)
            return Response(document)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
   except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def create_multiple_documents_view(request, dbname, type):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "major", type, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        documents_data = request.data
        documents = create_multiple_documents(db, documents_data)
        return Response(documents)
    
    except ConnectionError:
        try:
            backup_server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "replica",type , settings.COUCHDB_PORT)
            db = get_database(backup_server, dbname)
            documents_data = request.data
            documents = create_multiple_documents(db, documents_data)
            return Response(documents)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def add_database_to_server(request, type):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "major", type, settings.COUCHDB_PORT)
        dbname = request.data['dbname']
        create_database(server, dbname)
        response_data = {"message": "Database created successfully"}
        return Response(response_data, status=200)
    
    except ConnectionError:
        try:
            backup_server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "replica",type , settings.COUCHDB_PORT)
            dbname = request.data['dbname']
            create_database(backup_server, dbname)
            response_data = {"message": "Database created successfully"}
            return Response(response_data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['PUT'])
@renderer_classes([JSONRenderer])
def update_document_view(request, dbname, doc_id, type):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "major", type, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        document_data = request.data
        update_document(db, doc_id, document_data)
        response_data = {"message": "Document updated successfully"}
        return Response(response_data, status=200)
    
    except ConnectionError:
        try:
            backup_server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "replica",type , settings.COUCHDB_PORT)
            db = get_database(backup_server, dbname)
            document_data = request.data
            update_document(db, doc_id, document_data)
            response_data = {"message": "Document updated successfully"}
            return Response(response_data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['DELETE'])
@renderer_classes([JSONRenderer])
def delete_document_view(request, dbname, doc_id, type):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "major", type, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        delete_document(db, doc_id)
        response_data = {"message": "Document deleted successfully"}
        return Response(response_data, status=200)
    
    except ConnectionError:
        try:
            backup_server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "replica",type , settings.COUCHDB_PORT)
            db = get_database(backup_server, dbname)
            delete_document(db, doc_id)
            response_data = {"message": "Document deleted successfully"}
            return Response(response_data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def mongodb_query_view(request, dbname, type):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "major", type, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        query = request.data
        documents = mongo_query(db, query)
        return Response(documents)
    
    except ConnectionError:
        try:
            backup_server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "replica",type , settings.COUCHDB_PORT)
            db = get_database(backup_server, dbname)
            query = request.data
            documents = mongo_query(db, query)
            return Response(documents)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def mongodb_key_query_view(request, dbname, type):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "major", type, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        key = request.data
        documents = mongo_key_query(db, key)
        return Response(documents)
    
    except ConnectionError:
        try:
            backup_server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "replica",type , settings.COUCHDB_PORT)
            db = get_database(backup_server, dbname)
            key = request.data
            documents = mongo_key_query(db, key)
            return Response(documents)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def upload_twitter_from_file_to_corresponding_couchdb(request, type):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "major", type, settings.COUCHDB_PORT)
        
        twitter_income = server["twitter_income"]
        twitter_rental = server["twitter_rental"]
        twitter_mortgage = server["twitter_mortgage"]
        twitter_homeless = server["twitter_homeless"]
        
        db_dict = {"income": twitter_income, "rental": twitter_rental, "mortgage": twitter_mortgage, "homeless": twitter_homeless}
        
        upload_twitter_from_file(db_dict, "final_json.json")
        
        return Response({"message": "Twitter data uploaded successfully"}, status=200)
    except Exception as e:
        try:
            backup_server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "replica",type , settings.COUCHDB_PORT)
            
            twitter_income = backup_server["twitter_income"]
            twitter_rental = backup_server["twitter_rental"]
            twitter_mortgage = backup_server["twitter_mortgage"]
            twitter_homeless = backup_server["twitter_homeless"]
            
            db_dict = {"income": twitter_income, "rental": twitter_rental, "mortgage": twitter_mortgage, "homeless": twitter_homeless}
            
            upload_twitter_from_file(db_dict, "final_json.json")
            
            return Response({"message": "Twitter data uploaded successfully"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_mapreduce_result_view(request, homelessRelatedDbname , comparedDbname, type):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "major", type, settings.COUCHDB_PORT)
        homelessDb = get_database(server, homelessRelatedDbname)
        comparedDb = get_database(server, comparedDbname)
        homeless_documents = get_mapreduce_result(homelessDb, homelessRelatedDbname)
        compared_documents = get_mapreduce_result(comparedDb, comparedDbname)
        

        
        homeless_documents.sort(key=lambda x: x["gcc"][0])
        compared_documents.sort(key=lambda x: x["gcc"][0])
        
        homeless_list = [ homeless_document.get("amount") for homeless_document in homeless_documents]
        compared_list = [ compared_document.get("amount") for compared_document in compared_documents]    
        mapreduce_result = {homelessRelatedDbname: homeless_list, comparedDbname: compared_list}
        return Response(mapreduce_result)
    except Exception as e:
        try:
            backup_server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "replica",type , settings.COUCHDB_PORT)
            homelessDb = get_database(backup_server, homelessRelatedDbname)
            comparedDb = get_database(backup_server, comparedDbname)
            homeless_documents = get_mapreduce_result(homelessDb, homelessRelatedDbname)
            compared_documents = get_mapreduce_result(comparedDb, comparedDbname)
            

            
            homeless_documents.sort(key=lambda x: x["gcc"][0])
            compared_documents.sort(key=lambda x: x["gcc"][0])

            homeless_list = [ homeless_document.get("amount") for homeless_document in homeless_documents]
            compared_list = [ compared_document.get("amount") for compared_document in compared_documents]    
            mapreduce_result = {homelessRelatedDbname: homeless_list, comparedDbname: compared_list}
            return Response(mapreduce_result)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

@api_view(["POST"])
@renderer_classes([JSONRenderer])
def create_new_mastodon_mapreduce_view(request, dbname, type):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "major", type, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        mapreduce_result = create_new_mastodon_mapreduce(db, dbname)
        return Response(mapreduce_result)
    except Exception as e:
        try:
            backup_server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "replica",type , settings.COUCHDB_PORT)
            db = get_database(backup_server, dbname)
            mapreduce_result = create_new_mastodon_mapreduce(db, dbname)
            return Response(mapreduce_result)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
@api_view(["get"])
@renderer_classes([JSONRenderer])
def get_mastodon_mapreduce_result_view(request, type, dbname):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "major",type ,settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        mapreduce_result = get_mastodon_mapreduce_result(db, dbname)
        return Response(mapreduce_result)
    except Exception as e:
        try:
            backup_server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, "replica",type , settings.COUCHDB_PORT)
            db = get_database(backup_server, dbname)
            mapreduce_result = get_mastodon_mapreduce_result(db, dbname)
            return Response(mapreduce_result)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    


