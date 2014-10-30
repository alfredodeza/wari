import nosqlite
from os import path

collection = None

connection = None

def get_connection():
    db_path = path.expanduser('~/.waridb')
    return nosqlite.Connection(db_path)
