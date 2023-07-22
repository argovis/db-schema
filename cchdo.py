# usage: python cchdo.py
# creates empty collections in the argo db called cchdoMeta and cchdo with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

metacollection = 'cchdoMetax'
datacollection = 'cchdox'

db[metacollection].drop()
db.create_collection(metacollection)
db[datacollection].drop()
db.create_collection(datacollection)

cchdometaSchema = {
    "bsonType": "object",
    "required": ["_id", "date_updated_argovis", "data_type", "expocode", "cchdo_cruise_id", "woce_lines"],
    "properties":{
        "_id": {
            "bsonType": "string"
        },
        "date_updated_argovis": {
            "bsonType": "date"
        },
        "data_type": {
            "bsonType": "string"
        },
        "country": {
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
        "expocode": {
            "bsonType": "string"
        },
        "file_expocode": {
            "bsonType": "string"
        },
        "cchdo_cruise_id": {
            "bsonType": ["double", "int"]
        },
        "woce_lines": {
            "bsonType": "array",
            "items": {
                "bsonType": "string"
            }
        },
        "positioning_system": {
            "bsonType": "string"
        }
    }
}

cchdoSchema = {
    "bsonType": "object",
    "required": ["_id","metadata","geolocation","data","basin","timestamp", "data_info", "source", "station", "cast"],
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
        "btm_depth": {
            "bsonType": "double"
        },
        "file_hash": {
            "bsonType": "string"
        },
        "basin": {
            "bsonType": "int"
        },
        "timestamp": {
            "bsonType": ["date", "null"]
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
                    "cruise_url": {
                        "bsonType": "string",
                    }
                }
            }
        },
        "data_warning": {
            "bsonType": "array",
            "items": {
                "bsonType": "string",
                "enum": ["degenerate_levels", "missing_basin", "missing_location", "missing_timestamp"]
            }
        },        
        "station": {
            "bsonType": "string"
        },
        "cast": {
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
        },
        "data_info": {
            "bsonType": "array",
            "items": {
                "bsonType": "array",
                "items": {
                    "bsonType": ["string", "array"]
                }
            }
        }
    }
}

db.command('collMod',metacollection, validator={"$jsonSchema": cchdometaSchema}, validationLevel='strict')
db[metacollection].create_index([("woce_lines", 1)])
db[metacollection].create_index([("cchdo_cruise_id", 1)])

db.command('collMod',datacollection, validator={"$jsonSchema": cchdoSchema}, validationLevel='strict')
db[datacollection].create_index([("metadata", 1)])
db[datacollection].create_index([("timestamp", -1), ("geolocation", "2dsphere")])
db[datacollection].create_index([("timestamp", -1)])
db[datacollection].create_index([("geolocation", "2dsphere")])
db[datacollection].create_index([("source.source", 1)])

