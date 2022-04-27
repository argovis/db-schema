# usage: python grids-meta.py
# creates an empty, unindexed collection in the argo db called grids-meta with schema validation enforcement

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

db['grids-meta'].drop()
db.create_collection('grids-meta')

gridmetaSchema = {
    "bsonType": "object",
    "required": ["_id","units","levels","date_added"],
    "properties":{
        "_id": {
            "bsonType": "string"
        },
        "units": {
            "bsonType": "string"
        },
        "levels": {
            "bsonType": "array",
            "items": {
                "bsonType": ["double", "int"]
            }
        },
        "date_added": {
            "bsonType": "date"
        },
        "lonrange": {
            "bsonType": "array",
            "minItems": 2,
            "maxItems": 2,
            "items": {
                "bsonType": ["double", "int"]
            }
        },
        "latrange": {
            "bsonType": "array",
            "minItems": 2,
            "maxItems": 2,
            "items": {
                "bsonType": ["double", "int"]
            }
        },
        "timerange": {
            "bsonType": "array",
            "minItems": 2,
            "maxItems": 2,
            "items": {
                "bsonType": ["date"]
            }
        },
        "loncell": {
            "bsonType": ["double", "int"]
        },
        "latcell": {
            "bsonType": ["double", "int"]
        }
    }
}

db.command('collMod','grids-meta', validator={"$jsonSchema": gridmetaSchema}, validationLevel='strict')

