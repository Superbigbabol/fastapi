from pymongo.mongo_client import MongoClient
from normalizedata import normalized_data
uri = "mongodb+srv://wdbzf123:FzCqorV6UsPlR0Nn@cluster0.y2usz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri)
db = client['adcore']
payments_collection = db['payeedata']

try:
    result = payments_collection.insert_many(normalized_data)
    print(f"Successfully inserted {len(result.inserted_ids)} records.")
except Exception as e:
    print(f"Error during insertion: {e}")

for record in payments_collection.find():
    print(record)
