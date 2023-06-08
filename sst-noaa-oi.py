# usage: python sst-noaa-oi.py
# creates empty collections in the argo db with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

metacollection = 'noaaOIsstMeta'
datacollection = 'noaaOIsst'

db[metacollection].drop()
db.create_collection(metacollection)
db[datacollection].drop()
db.create_collection(datacollection)

sstMetaSchema = {
    "bsonType": "object",
    "required": ["_id", "data_type", "data_info", "date_updated_argovis", "timestamp", "source"],
    "properties":{ 
        "_id": {
            "bsonType": "string"
        },
        "data_type": {
            "bsonType": "string"
        },
        "data_info": {
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
        "timeseries" : {
            "bsonType": "array",
            "items": {
                "bsonType": "data"
            }
        }
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
        }
    }
}

sstSchema = {
    "bsonType": "object",
    "required": ["_id", "metadata", "geolocation", "basin", "timestamp", "data", "record_identifier", "class"],
    "properties": {
        "_id": {
            "bsonType": "string"
        },
        "metadata": {
            "bsonType": "array",
            "items": {
                "bsonType": "string"
            }
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
        "data": {
            "bsonType": "array",
            "items": {
                "bsonType": "array",
                "items": {
                    "bsonType": ["double", "int", "string", "null"]
                }
            }
        }
    }
}

db.command('collMod',metacollection, validator={"$jsonSchema": tcMetaSchema}, validationLevel='strict')
db[metacollection].create_index([("name", 1)])

db.command('collMod',datacollection, validator={"$jsonSchema": tcSchema}, validationLevel='strict')
db[datacollection].create_index([("geolocation", "2dsphere")])
