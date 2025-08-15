# libraries
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
import logging
from logging_config import setup_logging

# setup logging
setup_logging()
logger = logging.getLogger(__name__)

def send_data(url, clean_data_dir):

    # Create a new client and connect to the server
    client = MongoClient(url, server_api=ServerApi('1'))


   # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
    
        db = client['CHESS_PROJECT']
    
        file_name = {'match_information': f'.//{clean_data_dir}//match_history.json',
                     'player_information': f'.//{clean_data_dir}//player_profile.json'
                    }

        # create collections
        for collection_name, file in file_name.items():
            logger.info(f'Importing {collection_name}')
            collection = db[collection_name]
            with open(file, 'r') as f:
                data = json.load(f)   
            if isinstance(data, list):
                collection.insert_many(data)
            else:
                collection.insert_one(data)
            logger.info("Data imported successfully!")   
         
    except Exception as e:
        logger.error(e)

    finally:
        client.close()