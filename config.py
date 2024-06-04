# config file

NUMBER_EXTRACTOR = r'\d+\.\d+'
STD_HEAD = {'User-Agent' : 'Mozilla/5.0'}
CLS_SOLD = "POSITIVE ITALIC"
CLS_BEST_PRICE = "STRIKETHROUGH POSITIVE ITALIC"
TAG_TYPE = "span"


#MONGDO DB CONFIG

# Path to the MongoDB bin directory
PATH_TO_MONGO_BIN = r'C:\Program Files\MongoDB\Server\7.0\bin'
# Command to start MongoDB
START_MONGO_CMD = [PATH_TO_MONGO_BIN + r'\mongod.exe']

MAX_ATTEMPTS = 3
WAIT_TIME = 5 



