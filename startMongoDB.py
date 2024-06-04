import subprocess

# Path to the MongoDB bin directory
mongodb_bin_dir = r'C:\Program Files\MongoDB\Server\7.0\bin'

# Command to start MongoDB
command = [mongodb_bin_dir + r'\mongod.exe']

# Start MongoDB using subprocess
process = subprocess.Popen(command)


process.wait()

output, error = process.communicate()
print(output)
print(error)

import pymongo

try:
    # Try to connect to MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['pokeProducts'] # Access the admin database
    collection = db['logistics']
    data = {'name' : 'hidden fates etb', 'price' : 400}
    collection.insert_one(data)
    server_info = db.command('serverStatus')  # Execute a serverStatus command
    client.close()
    print("MongoDB is running.")
except pymongo.errors.ServerSelectionTimeoutError as e:
    print("MongoDB is not running.")

process.terminate()