import os
import pandas as pd
import json
from pymongo.mongo_client import MongoClient

class mongo_operation:
    __collection = None
    __database = None
    
    def __init__(self, client_url: str, database_name: str, collection_name: str = None, pem_file_path: str = None):
        self.client_url = client_url
        self.database_name = database_name
        self.collection_name = collection_name
        self.pem_file_path = pem_file_path
        
    def create_mongo_client(self):
        if self.pem_file_path:
            client = MongoClient(self.client_url,
                                 tls=True,
                                 tlsCertificateKeyFile=self.pem_file_path)
        else:
            client = MongoClient(self.client_url)
        return client
    
    def create_database(self):
        if mongo_operation.__database is None:
            client = self.create_mongo_client()
            self.database = client[self.database_name]
        return self.database 
    
    def create_collection(self):
        if mongo_operation.__collection is None:
            database = self.create_database()
            self.collection = database[self.collection_name]
            mongo_operation.__collection = self.collection
        elif mongo_operation.__collection != self.collection_name:
            database = self.create_database()
            self.collection = database[self.collection_name]
            mongo_operation.__collection = self.collection
        return self.collection
    
    def insert_record(self, record: dict, collection_name: str):
        if isinstance(record, list):
            for data in record:
                if not isinstance(data, dict):
                    raise TypeError("Each record must be a dictionary")
            collection = self.create_collection()
            collection.insert_many(record)
        elif isinstance(record, dict):
            collection = self.create_collection()
            collection.insert_one(record)
    
    def bulk_insert(self, datafile):
        self.path = datafile
        
        if self.path.endswith('.csv'):
            dataframe = pd.read_csv(self.path, encoding='utf-8')
        elif self.path.endswith(".xlsx"):
            dataframe = pd.read_excel(self.path, encoding='utf-8')
        else:
            raise ValueError("Unsupported file format. Only .csv and .xlsx are supported.")
        
        datajson = json.loads(dataframe.to_json(orient='records'))
        collection = self.create_collection()
        collection.insert_many(datajson)
