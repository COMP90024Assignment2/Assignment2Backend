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
server = connect_to_couchdb(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, 
                             settings.COUCHDB_HOST, settings.COUCHDB_PORT)
db = create_database(server, settings.COUCHDB_DBNAME)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_all_documents_view(request):
    try:
        couchdb_url = get_couchdb_url(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, settings.COUCHDB_HOST, settings.COUCHDB_PORT)
        couchdb_request = f"{couchdb_url}/{settings.COUCHDB_DBNAME}/_all_docs?include_docs=true"
        response = requests.get(couchdb_request)

        if response.status_code == 200:
            data = response.json()
            tasks = [row['doc'] for row in data['rows']]
            return Response(tasks)
        else:
            return Response(response.json(), status=response.status_code)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_document_view(request, doc_id):
    try:
        couchdb_url = get_couchdb_url(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, settings.COUCHDB_HOST, settings.COUCHDB_PORT)
        couchdb_request = f"{couchdb_url}/{settings.COUCHDB_DBNAME}/{doc_id}"
        response = requests.get(couchdb_request)

        if response.status_code == 200:
            data = response.json()
            return Response(data)
        else:
            return Response(response.json(), status=response.status_code)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def create_document_view(request):
    try:
        document_data = request.data
        couchdb_url = get_couchdb_url(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, settings.COUCHDB_HOST, settings.COUCHDB_PORT)
        couchdb_request = f"{couchdb_url}/{settings.COUCHDB_DBNAME}"
        response = requests.post(couchdb_request, json=document_data)

        if response.status_code == 201:
            data = response.json()
            return Response(data)
        else:
            return Response(response.json(), status=response.status_code)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def add_node_to_cluster():
    try:
        node_data = request.data
        couchdb_url = get_couchdb_url(settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD, settings.COUCHDB_HOST, settings.COUCHDB_PORT)





export declare nodes=(172.26.135.33 172.26.132.58 172.26.130.194 172.26.135.182)
export masternode=`echo ${nodes} | cut -f1 -d' '`
export declare othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export size=${#nodes[@]}
export user='admin'
export pass='admin'
export VERSION='3.2.1'
export cookie='63629434aa894546fdba2608ab28efe8'