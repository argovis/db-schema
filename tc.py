# usage: python tc.py
# creates empty collections in the argo db called tcMeta and tc with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

metacollection = 'tcMeta'
datacollection = 'tc'

db[metacollection].drop()
db.create_collection(metacollection)
db[datacollection].drop()
db.create_collection(datacollection)

tcMetaSchema = {
    "bsonType": "object",
    "required": ["_id", "data_type", "measurement_metadata", "date_updated_argovis", "source", "name", "num"],
    "properties":{ 
        "_id": {
            "bsonType": "string"
        },
        "data_type": {
            "bsonType": "string"
        },
        "measurement_metadata": {
            "bsonType": "array",
            "items": {
                "bsonType": "array",
                "items": {
                    "bsonType": ["string", "array"]
                }
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
            "bsonType": "object",
            "properties": {x: {"bsonType": "array", "items": {"bsonType": ["double", "int", "string", "null"]}} for x in ['wind', 'surface_pressure']}
        },
        "record_identifier": {
            "bsonType": "string"
        },
        "class": {
            "bsonType": "string"
        }
    }
}

db.command('collMod',metacollection, validator={"$jsonSchema": tcMetaSchema}, validationLevel='strict')
db[metacollection].create_index([("name", 1)])

db.command('collMod',datacollection, validator={"$jsonSchema": tcSchema}, validationLevel='strict')
db[datacollection].create_index([("metadata", 1)])
db[datacollection].create_index([("timestamp", -1), ("geolocation", "2dsphere")])
db[datacollection].create_index([("timestamp", -1)])
db[datacollection].create_index([("geolocation", "2dsphere")])
