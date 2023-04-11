import gridfs
import pymongo
from django.db import connection


mongo_db  = pymongo.MongoClient()
db_name = connection.settings_dict['NAME']

def saveFile(_file):
    'Save document in database with verification'
    print(db_name)
    # # 1 - Store document in GridFS
    fs = gridfs.GridFS(mongo_db[db_name])        
    docID = str(fs.put(_file)) 
    
    return docID