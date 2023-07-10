from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class DBConnector:
    def __init__(self, db_name = 'RobotTaskGenerationDB'):
        debug = False
        # Atlas connection string
        uri = 'mongodb+srv://swiechmaciek:swiechmaciek@robottaskgenerationclus.sztqyuy.mongodb.net/?retryWrites=true&w=majority'
        
        # Set the Stable API version when creating a new client
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Print databases present in the cluster
        if debug:
            cursor = self.client.list_databases()
            for db in cursor:
                print(db)
        self.db = self.client[db_name]
        
        # Send a ping to confirm a successful connection
        if debug:
            try:
                self.client.admin.command('ping')
                print('Pinged your deployment. You successfully connected to MongoDB!')
            except Exception as e:
                print(e)
                
    def get_collection_names(self):
        return self.db.list_collection_names()

    def get_data_from_collection(self, collection_name):
        collection = self.db[collection_name]
        return collection.find()
    
    def get_tasks_system_can_perform(self, collection_name = 'RobotAbilities'):
        tasks_system_can_perform = []
        for ability_dict in list(self.get_data_from_collection(collection_name)):
            tasks_system_can_perform.append(ability_dict['name'])
        return tasks_system_can_perform

dbc = DBConnector()
