import couchdb
from couchdb.client import Document
from django.conf import settings
import json
import ijson
def get_couchdb_url(username, password, role, port):

    host = settings.COUCHDB_HOST[role]
    
    return f'http://{username}:{password}@{host}:{port}/'

def connect_to_couchdb(username, password, role, port):
    
    host = settings.COUCHDB_HOST[role]
    
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
    
def mongo_key_query(db,key):
    result = []
    for doc_id in db:
        doc = db[doc_id]
        if key in doc:
            result.append(doc)
    return result

# def upload_twitter_from_file(db_dict, file_name):
#     with open(file_name, "r", encoding="UTF-8") as json_file:
#         json_file.readline()
#         while True:
#             try:
#                 current_line = json_file.readline()
#                 if current_line == "]" or current_line == "\n" or current_line == "":
#                     break
#                 else:
#                     current_line = current_line[:-2]
#                     json_object = json.loads(current_line)
#                     if "homeless" in json_object:
#                         db_dict["homeless"].save(json_object)
#                     if "income" in json_object:
#                         db_dict["income"].save(json_object)
#                     if "rental" in json_object:
#                         db_dict["rental"].save(json_object)
#                     if "mortgage" in json_object:
#                         db_dict["mortgage"].save(json_object)
#             except json.JSONDecodeError:
#                 print(f'Error decoding JSON for line: {current_line}')
#                 continue  # skip to the next line

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
            
def get_mapreduce_result(db, design_doc_id, view_name):

    # design_doc_id = 'twitter_rental_full_name'
    # view_name = 'twitter_rental_full_name'
    design_doc_id = '_design/' + design_doc_id
    view_name = '_view/' + view_name
    view = db.view(f'{design_doc_id}/{view_name}', group=True)
    documents = []
    #documents = [ documents.append({"gcc": row.key, "amount": row.value}) for row in view]
    for row in view:
        documents.append({"gcc": row.key, "amount": row.value})
    return documents