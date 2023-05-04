import couchdb

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

def get_document(db, doc_id):
    return db.get(doc_id)

def get_all_documents(db) -> list:
    return db.view('_all_docs', include_docs=True)


def query_document(db, key) -> list:
    return db.view('_all_docs', key=key, include_docs=True)
    
def create_document(db, doc):
    pass

def save_document(db, doc):
    db.save(doc)

def update_document(db, doc_id, new_data):
    doc = db.get(doc_id)
    if doc:
        doc.update(new_data)
        db.save(doc)

def delete_document(db, doc_id):
    doc = db.get(doc_id)
    if doc:
        db.delete(doc)