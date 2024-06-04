
import datetime
import socket
import subprocess
import time


import config #local
from classes.pokeProduct import pokeProduct

from pymongo import MongoClient, errors
import pandas as pd



def main():

    if is_mongo_running():
        print("MongoDB is already running.")
        etl()
        
    else:
        curr_process = run_mongo()
        etl()
        curr_process.terminate()
    print('d')




    #generator for memory
def iterate_documents(cursor):
    for document in cursor:
        yield document

def etl() :
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['pokeProducts']

        current_datetime = datetime.datetime.now() # create a new collection
        collection_name = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        db.create_collection(collection_name)
        new_collection = db[collection_name]


        persistent_collection = db["JiMinRyu"]  # get all documents and scrape them one by one and throw them back in the DB
        cursor = persistent_collection.find()
        for document in iterate_documents(cursor):
            data = {}
            for field, value in document.items(): # get all fields
                if field != '_id':
                    data[field] = value
            product = pokeProduct(**data) # instatiating the class will call the scraper

            new_data = product.get_data() # get the new data
            new_collection.insert_one(new_data) #insert new data

        new_cursor = new_collection.find({}, {'_id': 0}) 
        df = pd.DataFrame(list(new_cursor))
        df.to_excel(collection_name + ".xlsx", index = False)




        server_info = db.command('serverStatus')  # Execute a serverStatus command
        print(server_info)
        client.close()
        print("MongoDB is running.")
    except errors.ServerSelectionTimeoutError as e:
        print("MongoDB is not running.")


def is_mongo_running() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Check if MongoDB port is in use (default port is 27017)
        return s.connect_ex(('localhost', 27017)) == 0

def run_mongo() -> subprocess:

    attempt = 0
    while attempt < config.MAX_ATTEMPTS:
        attempt += 1
        print(f"Attempting to start MongoDB (Attempt {attempt}/{config.MAX_ATTEMPTS})...")
        
        # Start MongoDB subprocess
        process = subprocess.Popen(config.START_MONGO_CMD)
        process.wait()

        # Check if MongoDB started successfully
        if process.returncode == 0:
            print("MongoDB started successfully.")
            return process
        else:
            print("Failed to start MongoDB.")

        # Wait before the next attempt
        time.sleep(config.WAIT_TIME)

    print("Maximum number of attempts reached. MongoDB could not be started.")
    return False


main()







