import os
import pymongo

from configs.config import mongo_server_host
from configs.config import mongo_bhashadaan_db
from configs.config import mongo_col

mongo_instance = None

class Repository:

    def __init__(self):
        pass

    # Initialises and fetches mongo client
    def instantiate(self):
        client = pymongo.MongoClient(mongo_server_host)
        db = client[mongo_bhashadaan_db]
        mongo_instance = db[mongo_col]
        return mongo_instance

    def get_mongo_instance(self):
        if not mongo_instance:
            return self.instantiate()
        else:
            return mongo_instance

    #Get user details: 
    def get_user_details(self,query):
        col = self.get_mongo_instance()
        res = col.find(query,{}).sort([('_id', 1)])
        result = []
        for record in res:
            result.append(record)
        return result

    # Inserts the object into mongo collection
    def create_entry(self, object_in):
        col = self.get_mongo_instance()
        col.insert_one(object_in)

    # Updates the object in the mongo collection
    def update_entry(self, object_in, phone_number):
        col = self.get_mongo_instance()
        result = col.update_many(
            {"_id": phone_number},
            object_in
        )

    # Searches the object into mongo collection
    def search_entry(self, query, exclude={}, offset=None, res_limit=None):
        col = self.get_mongo_instance()
        if offset is None and res_limit is None:
            res = col.find(query, exclude).sort([('_id', 1)])
        else:
            res = col.find(query, exclude).sort([('_id', -1)]).skip(offset).limit(res_limit)
        result = []
        for record in res:
            result.append(record)
        return result
