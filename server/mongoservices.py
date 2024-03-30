from typing import List, Union
import pymongo
from pymongo.errors import ServerSelectionTimeoutError

import os


class Mongo:
    def __init__(self, collection, Mongo_url):
        """
        Initializes the Mongo object by connecting to the MongoDB database,
        accessing the "TrustVault" database, and the "CIDs" collection.
        """
        self.client = pymongo.MongoClient(Mongo_url)

        # database = reddit
        self.db = self.client['reddit']
        self.collection = self.db.get_collection(collection)
    
    def insert(self, data: dict) -> bool:
        """
        Inserts a new document into the collection with the provided data.

        Args:
            data (dict): The data to insert.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            self.collection.insert_one(data)
            return True
        except Exception as e:
            print(e)
            return False
        
    def read(self) -> List[dict] :
        """
        Reads all the documents from the "CIDs" collection.

        Returns:
            List[dict]: A list of dictionaries containing the user and CID(s).
        """
        try:
            cursor = self.collection.find()
            cid = []
            for document in cursor:
                cid.extend(document["cid"])
            return cid
        except Exception as e:
            print(e)
            return []

    def drop_collection(self) -> bool:
        """
        Drop the current collection
        """
        try:
            self.collection.drop()
            return True
        except Exception as e:
            print("Exception: ",e)
            return False
        
def is_valid_mongo_url(mongo_url):
    try:
        client = pymongo.MongoClient(mongo_url, serverSelectionTimeoutMS=4000)
        client.admin.command('ismaster')
        return True
    except ServerSelectionTimeoutError:
        return False