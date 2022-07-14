# usage: python grids.py <grid name>
# creates an empty, unindexed collection in the argo db called <grid name> with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

grid = sys.argv[1]
client = MongoClient('mongodb://database/argo')
db = client.argo

db[grid].drop()
db.create_collection(grid)

gridSchema = {
    "bsonType": "object",
    "required": ["_id", "metadata","geolocation","data","basin","timestamp"],
    "properties": {
        "_id": {
            "bsonType": "string"
        },
        "metadata": {
            "bsonType": "string"
        },
        "geolocation": {
            "bsonType": "object",
            "required": ["type", "coordinates"],
            "properties": {
                "type":{
                    "enum": ["Point"]
                },
                "coordinates":{
                    "bsonType": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {
                        "bsonType": ["double", "int"]
                    }
                }
            }
        },
        "basin": {
            "bsonType": "int"
        },
        "timestamp": {
            "bsonType": ["date", "null"]
        },
        "data": {
            "bsonType": "array",
            "items": {
                "bsonType": "array",
                "items": {
                    "bsonType": ["double", "int", "null"]
                }
            }
        }
    }
}

db.command('collMod',grid, validator={"$jsonSchema": gridSchema}, validationLevel='strict')
db[grid].create_index([("metadata", 1)])
db[grid].create_index([("timestamp", -1), ("geolocation", "2dsphere")])
db[grid].create_index([("geolocation", "2dsphere")])

