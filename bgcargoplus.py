# usage: python argo.py
# creates empty collections in the argo db called argoMeta and argo with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

metacollection = 'bgcargoplusMeta'
datacollection = 'bgcargoplus'

db[metacollection].drop()
db.create_collection(metacollection)
db[datacollection].drop()
db.create_collection(datacollection)

bgcargoplusMetaSchema = {
    "bsonType": "object",
    "required": ["_id", "data_type"],
    "properties":{
        "_id": {
            "bsonType": "string"
        },
        "data_type": {
            "bsonType": "string"
        },
        "data_center": {
            "bsonType": "string"
        },
        "instrument": {
            "bsonType": "string"
        },
        "pi_name": {
            "bsonType": "array",
            "items": {
                "bsonType": "string"
            }
        },
        "platform": {
            "bsonType": "string"
        },
        "platform_type": {
            "bsonType": "string"
        },
        "fleetmonitoring": {
            "bsonType": "string"
        },
        "oceanops": {
            "bsonType": "string"
        },
        "positioning_system": {
            "bsonType": "string"
        },
        "wmo_inst_type": {
            "bsonType": "string"
        }
    }
}

bgcargoplusSchema = {
    "bsonType": "object",
    "required": ["_id","metadata","geolocation","basin","timestamp","data", "date_updated_argovis", "source", "cycle_number"],
    "properties": {
        "_id": {
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
                    "doi": {
                        "bsonType": "string",
                    }
                }
            }
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
        "cycle_number": {
            "bsonType": "int"
        },
        "geolocation_argoqc": {
            "bsonType": "int"
        },
        "profile_direction": {
            "bsonType": "string"
        },
        "timestamp_argoqc": {
            "bsonType": "int"
        },
        "metadata": {
            "bsonType": "array",
            "items": {
                "bsonType": "string"
            }
        },
        "data": {
            "bsonType": "array",
            "items": {
                "bsonType": "array",
                "items": {
                    "bsonType": ["double", "int", "string", "null"]
                }
            }
        },
    }
}

db.command('collMod',metacollection, validator={"$jsonSchema": bgcargoplusMetaSchema}, validationLevel='strict')
db[metacollection].create_index([("data_center", 1)])
db[metacollection].create_index([("platform", 1)])
db[metacollection].create_index([("platform_type", 1)])

db.command('collMod',datacollection, validator={"$jsonSchema": bgcargoplusSchema}, validationLevel='strict')
db[datacollection].create_index([("metadata", 1)])
db[datacollection].create_index([("timestamp", -1), ("geolocation", "2dsphere")])
db[datacollection].create_index([("timestamp", -1)])
db[datacollection].create_index([("geolocation", "2dsphere")])
db[datacollection].create_index([("geolocation.coordinates", "2d"), ("timestamp", -1)])
db[datacollection].create_index([("geolocation_argoqc", 1)])
