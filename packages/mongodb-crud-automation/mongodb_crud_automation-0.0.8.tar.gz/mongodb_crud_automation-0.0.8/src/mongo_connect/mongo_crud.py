from typing import Any
import os
import pymongo
from ensure import ensure_annotations
from pymongo.mongo_client import MongoClient
import pandas as pd
import json 

class mongodb_operation:
    @ensure_annotations 
    def __init__(self,client_url: str,database_name: str,collection_name: str=None):
        self.client_url = client_url
        self.database_name = database_name
        self.collection_name = collection_name
        
    @ensure_annotations 
    def create_client(self):
        client = MongoClient(self.client_url)
        return client 
        
    @ensure_annotations 
    def create_database(self):
        client = self.create_client()
        database = client[self.database_name]
        return database
        
    @ensure_annotations 
    def create_collection(self,collection= None):
        database = self.create_database()
        collection = database[collection]
        return collection
        
    @ensure_annotations 
    def insert_record(self,record: dict,collection_name: str):
        if type(record)==list:
            for data in record:
                if type(data)!=dict:
                    raise TypeError("record must be in the dict")
            collection = self.create_collection(collection_name)
            collection.insert_many(record)

        elif type(record)==dict:
            collection = self.create_collection(collection_name)
            collection.insert_one(record)
            
    @ensure_annotations 
    def bulk_insert(self,datafile: str,collection_name: str=None,unique_field: str = None):
        self.path = datafile

        if self.path.endswith('.csv'):
            data = pd.read_csv(self.path,encoding='utf-8')

        elif self.path.endswith('.xlsx'):
            data = pd.read_excel(self.path,encoding='utf-8')

        data_json = json.loads(data.to_json(orient = 'record'))
        collection = self.create_collection()

        if unique_field:
            for record in data_json:
                if collection.count_documents({unique_field: record[unique_field]}) == 0:
                    collection.insert_one(record)
                else:
                    print(f"Record with {unique_field}={record[unique_field]} already exists. Skipping insertion.")
        else:
            collection.insert_many(data_json)
        
    @ensure_annotations 
    def find(self, query: dict = {}, collection_name: str = None):
        collection = self.create_collection(collection_name)
        results = collection.find(query)
        return list(results)
        
    @ensure_annotations 
    def update(self, query: dict, new_values: dict, collection_name: str = None):
        collection = self.create_collection(collection_name)
        collection.update_many(query, {"$set": new_values})
        
    @ensure_annotations 
    def delete(self, query: dict, collection_name: str = None):
        collection = self.create_collection(collection_name)
        collection.delete_many(query)
    
