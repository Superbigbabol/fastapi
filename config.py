
from pymongo.mongo_client import MongoClient
# URL = "mongodb+srv://wdbzf123:FzCqorV6UsPlR0Nn@cluster0.y2usz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# db = client['adcore']
# payments_collection = db['payeedata']
# db connection
USERNAME = "wdbzf123"
PASSWORD = "FzCqorV6UsPlR0Nn"
URL = "mongodb+srv://{0}:{1}@cluster0.y2usz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0".format(USERNAME, PASSWORD)

try:
    conn = MongoClient(URL)
    print("Mongodb Connected", conn)
    db = conn['adcore']
    collection = db['payeedata']
except Exception as e:
    print(f"Error in mongodb connection: {e}")
