import couchdb
from couchdb.client import Document
import json
def get_couchdb_url(username, password, host, port):
    return f'http://{username}:{password}@{host}:{port}/'

def connect_to_couchdb(username, password, host, port):
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
    if dbname in server:
        return server[dbname]
    else:
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
    
    
