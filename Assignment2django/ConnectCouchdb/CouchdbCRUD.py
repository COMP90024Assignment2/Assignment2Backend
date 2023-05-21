import couchdb
from couchdb.client import Document
from django.conf import settings
import json
import ijson
def get_couchdb_url(username, password, role, type,  port):

    host = settings.COUCHDB_HOST[role][type]
    
    return f'http://{username}:{password}@{host}:{port}/'

def connect_to_couchdb(username, password, role, type, port):
    
    host = settings.COUCHDB_HOST[role][type]
    
    url = f'http://{username}:{password}@{host}:{port}/'
    server = couchdb.Server(url)
    return server

def create_database(server, dbname):
    try:
        db = server.create(dbname)
    except couchdb.http.PreconditionFailed:
        db = server[dbname]
    return db

def delete_database(server, dbname):
    if dbname in server:
        del server[dbname]
    else:
        raise Exception("Database not found")
    
def get_database(server, dbname):
    try:
        if dbname in server:
            return server[dbname]
    except Exception as e:
        print(e)
        raise Exception("Database not found")
        
        

def get_document(db, doc_id) -> dict:
    return db.get(doc_id)

def get_all_documents(db) -> list:
    all_doc = db.view('_all_docs', include_docs=True)
    documents = [row["doc"] for row in all_doc]
    return documents


def query_document(db, key) -> list:
    return db.view('_all_docs', key=key, include_docs=True)
    
def create_document(db, doc):
    return db.save(doc)

def create_multiple_documents(db, docs):
    wrapped_docs = [Document(doc) for doc in docs]
    return db.update(wrapped_docs)

def save_document(db, doc):
    db.save(doc)

def update_document(db, doc_id, new_data):
    doc = db.get(doc_id)
    if doc:
        doc.update(new_data)
        db.save(doc)
    else:
        raise Exception("Document not found")

def delete_document(db, doc_id):
    doc = db.get(doc_id)
    if doc:
        db.delete(doc)
    else:
        raise Exception("Document not found")
    
def get_view(db, view_name):
    return db.view(view_name)

def create_view(db, view_name, map_fun, reduce_fun):
    db[view_name] = couchdb.design.ViewDefinition(view_name, map_fun, reduce_fun)
    
def mongo_query(db,json_object):
    required_keys = json_object.keys()
    keys_values_str = ""
    for key in required_keys:
        keys_values_str += "\"" + key + "\": {\"$eq\": \"" + json_object[key] + "\"},"
    keys_values_str = keys_values_str[:-1]
    mongo_query_json_str = "{\"selector\": {" + keys_values_str + "}}"
    new_json_object = json.loads(mongo_query_json_str)
    result = db.find(new_json_object)
    return result
    
def mongo_key_query(db,key):
    result = []
    for doc_id in db:
        doc = db[doc_id]
        if key in doc:
            result.append(doc)
    return result



def upload_twitter_from_file(db_dict, file_name):
    with open(file_name, 'r', encoding='UTF-8') as json_file:
        # use ijson to iteratively parse the json file
        objects = ijson.items(json_file, 'item')

        for json_object in objects:
            try:
                if "homeless" in json_object:
                    db_dict["homeless"].save(json_object)
                if "income" in json_object:
                    db_dict["income"].save(json_object)
                if "rental" in json_object:
                    db_dict["rental"].save(json_object)
                if "mortgage" in json_object:
                    db_dict["mortgage"].save(json_object)
            except Exception as e:
                print(f'Error processing JSON object: {e}')
                continue  # skip to the next object
            
def get_mapreduce_result(db, dbname):
    gcc_list = ['1gsyd','2gmel' ,'3gbri', '4gade' , '5gper', '6ghob' , '7gdar', '8acte']
    mapreduce = f'_design/{dbname}_design/_view/{dbname}_view'

    view = db.view(mapreduce, group=True)
    documents = []
    for row in view:
        if (row.key in gcc_list):
            documents.append({"gcc": row.key, "amount": row.value})
        else:
            documents.append({"gcc": "nan", "amount": row.value})
            
        
    return documents

def get_mastodon_mapreduce_result(db, dbname):
    mapreduce = f'_design/{dbname}_design/_view/{dbname}_view'

    view = db.view(mapreduce, group=True)
    documents = []
    for row in view:
        documents.append({"date": row.key, "amount": row.value})
        
    return documents

def create_new_mastodon_mapreduce(server, dbname):
    
    db = server[dbname]

    map_function = '''function (doc) {
        var date = new Date(doc.created_at);
        var year = date.getFullYear();
        var month = (1 + date.getMonth()).toString().padStart(2, '0');
        var day = date.getDate().toString().padStart(2, '0');
        emit(year + '-' + month + '-' + day, 1);
    }'''

    reduce_function = '_sum'

    design = {
        '_id': '_design/{dbname}_test'.format(dbname=dbname),
        'views': {
            '{dbname}_test'.format(dbname=dbname): {
                'map': map_function,
                'reduce': reduce_function
            }
        }
    }

    try:
        db.save(design)
    except couchdb.http.ResourceConflict:
        old = db['_design/{dbname}_test'.format(dbname=dbname)]
        design['_rev'] = old.rev
        db.save(design)

    
        
        
    