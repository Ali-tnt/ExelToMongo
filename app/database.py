from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "exelToMongoDB")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "phoneNumbers")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Create index on phone numbers for better performance
async def init_db():
    await collection.create_index("mobile", unique=True)