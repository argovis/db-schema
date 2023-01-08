# usage: python grids-meta.py
# creates an empty, unindexed collection in the argo db called grids-meta with schema validation enforcement

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

metacollection = 'gridMetax'

db[metacollection].drop()
db.create_collection(metacollection)

gridmetaSchema = {
    "bsonType": "object",
    "required": ["_id", "data_type", "date_updated_argovis", "source", "levels"],
    "properties":{
        "_id": {
            "bsonType": "string"
        },
        "data_type": {
            "bsonType": "string"
        },
        "date_updated_argovis": {
            "bsonType": "date"
        },
        "source": {
            "bsonType": "array",
            "items": {
                "bsonType": "object",
                "required": ["source"],
                "properties": {
                    "source": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "string"
                        }
                    },
                    "url": {
                        "bsonType": "string",
                    },
                    "doi": {
                        "bsonType": "string",
                    },
                    "date_updated": {
                        "bsonType": "date",
                    }
                }
            }
        },
        "levels": {
            "bsonType": "array",
            "items": {
                "bsonType": ["double", "int"]
            }
        }
    }
}

db.command('collMod',metacollection, validator={"$jsonSchema": gridmetaSchema}, validationLevel='strict')

