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

# Connect to CouchDB


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_all_documents_view(request, dbname):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, settings.COUCHDB_HOST, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        documents = get_all_documents(db)
        return Response(documents)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_document_view(request, dbname ,doc_id):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, settings.COUCHDB_HOST, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        document = get_document(db, doc_id)
        return Response(document)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def create_document_view(request, dbname):
   try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, settings.COUCHDB_HOST, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        document_data = request.data
        print(document_data)
        document = create_document(db, document_data)
        return Response(document)
   except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def create_multiple_documents_view(request, dbname):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, settings.COUCHDB_HOST, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        documents_data = request.data
        documents = create_multiple_documents(db, documents_data)
        return Response(documents)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def add_database_to_server(request):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, settings.COUCHDB_HOST, settings.COUCHDB_PORT)
        dbname = request.data['dbname']
        create_database(server, dbname)
        response_data = {"message": "Database created successfully"}
        return Response(response_data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['PUT'])
@renderer_classes([JSONRenderer])
def update_document_view(request, dbname, doc_id):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, settings.COUCHDB_HOST, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        document_data = request.data
        update_document(db, doc_id, document_data)
        response_data = {"message": "Document updated successfully"}
        return Response(response_data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['DELETE'])
@renderer_classes([JSONRenderer])
def delete_document_view(request, dbname, doc_id):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, settings.COUCHDB_HOST, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        delete_document(db, doc_id)
        response_data = {"message": "Document deleted successfully"}
        return Response(response_data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def mongodb_query_view(request, dbname):
    try:
        server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, settings.COUCHDB_HOST, settings.COUCHDB_PORT)
        db = get_database(server, dbname)
        query = request.data
        documents = mongo_query(db, query)
        return Response(documents)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

