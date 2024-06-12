from typing import Any
import os 
import pandas as pd
from pymongo import MongoClient
import pymongo
import json
from ensure import ensure_annotations


class mongo_operation:
    __collection = None
    __database = None

    def __init__(self, client_url:str, database_name: str, collection_name:str = None):
        self.client_url = client_url
        self.database_name = database_name
        self.collection_name = collection_name

    def create_mongo_client(self, collection=None):
        client = MongoClient(self.client_url)
        return client
    
    def create_collection(self, collection=None):
        if mongo_operation.__collection==None or mongo_operation.__collection != collection:
            database = self.create_collection(collection)
            self.collection = database[self.collection_name]
            mongo_operation.__collection = collection

        return self.collection
    
    def insert_record(self, record:dict, collection_name:str) -> Any:
        if type(record) == list:
            for data in record:
                if type(data) != dict:
                    raise TypeError("Record must be in the dict")
            collection = self.create_collection(collection_name)
            collection.insert_many(record)
        elif type(record) == dict:
            collection = self.create_collection(collection_name)
            collection.insert_one(record)

    def bulk_insert(self, datafile: str, collection_name:str = None):
        if collection_name == None:
            collection_name = self.collection_name

        self.path = datafile

        if self.path.endswith('.csv'):
            data = pd.read_csv(self.path, encoding='utf-8')
        elif self.path.endswith('.xlsx'):
            data = pd.read_excel(self.path)
        else:
            raise ValueError("Unsupported file format. Only .csv and .xlsx are supported.")

        datajson = json.loads(data.to_json(orient='records'))
        collection = self.create_collection(collection_name)
        collection.insert_many(datajson)
        