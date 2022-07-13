# usage: python grids-meta.py
# creates an empty, unindexed collection in the argo db called grids-meta with schema validation enforcement

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

db['gridMetax'].drop()
db.create_collection('gridMetax')

gridmetaSchema = {
    "bsonType": "object",
    "required": ["_id", "data_type", "data_keys", "units", "date_updated_argovis", "source", "levels", "lonrange", "latrange", "timerange", "loncell", "latcell"],
    "properties":{
        "_id": {
            "bsonType": "string"
        },
        "data_type": {
            "bsonType": "string"
        },
        "data_keys": {
            "bsonType": "array",
            "items": {
                "bsonType": "string"
            }
        },
        "units": {
            "bsonType": "array",
            "items": {
                "bsonType": ["string", "null"]
            }
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
                    }
                }
            }
        },
        "levels": {
            "bsonType": "array",
            "items": {
                "bsonType": ["double", "int"]
            }
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

db.command('collMod','gridMetax', validator={"$jsonSchema": gridmetaSchema}, validationLevel='strict')

