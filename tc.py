# usage: python tc.py
# creates empty collections in the argo db called tcMeta and tc with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

db['tcMeta'].drop()
db.create_collection('tcMeta')
db['tc'].drop()
db.create_collection('tc')

tcMetaSchema = {
    "bsonType": "object",
    "required": ["_id", "data_type", "data_keys", "units", "date_updated_argovis", "source", "name", "num"],
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
                    }
                }
            }
        },
        "name": {
            "bsonType": "string"
        },
        "num": {
            "bsonType": "int"
        }
    }
}

tcSchema = {
    "bsonType": "object",
    "required": ["_id", "metadata", "geolocation", "basin", "timestamp", "data", "record_identifier", "class"],
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
        },
        "record_identifier": {
            "bsonType": "string"
        },
        "class": {
            "bsonType": "string"
        }
    }
}

db.command('collMod','tcMeta', validator={"$jsonSchema": tcMetaSchema}, validationLevel='strict')
db['tc'].create_index([("name", 1)])

db.command('collMod','tc', validator={"$jsonSchema": tcSchema}, validationLevel='strict')
db['tc'].create_index([("metadata", 1)])
db['tc'].create_index([("timestamp", -1), ("geolocation", "2dsphere")])
db['tc'].create_index([("geolocation", "2dsphere")])
