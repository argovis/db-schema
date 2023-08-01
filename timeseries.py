# generic timeseries schema
# usage: python timeseries.py [series data collection name, like 'noaaOIsst', 'copernicusSLA' or 'ccmp']
# creates empty collections in the argo db with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

metacollection = sys.argv[1] + 'Meta'
datacollection = sys.argv[1]

db[metacollection].drop()
db.create_collection(metacollection)
db[datacollection].drop()
db.create_collection(datacollection)

metaSchema = {
    "bsonType": "object",
    "required": ["_id", "data_type", "data_info", "date_updated_argovis", "timeseries", "source"],
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
                "bsonType": "date"
            }
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
        }
    }
}

dataSchema = {
    "bsonType": "object",
    "required": ["_id", "metadata", "geolocation", "basin", "data"],
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

db.command('collMod',metacollection, validator={"$jsonSchema": metaSchema}, validationLevel='strict')

db.command('collMod',datacollection, validator={"$jsonSchema": dataSchema}, validationLevel='strict')
db[datacollection].create_index([("geolocation", "2dsphere")])
