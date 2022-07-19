# usage: python goship.py
# creates empty collections in the argo db called goshipMeta and goship with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

db['goshipMeta'].drop()
db.create_collection('goshipMeta')
db['goship'].drop()
db.create_collection('goship')

goshipmetaSchema = {
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
        "cchdo_cruise_id": {
            "bsonType": "string"
        },
        "woce_lines": {
            "bsonType": "array",
            "items": {
                "bsonType": "string"
            }
        }
    }
}

goshipSchema = {
    "bsonType": "object",
    "required": ["_id","metadata","geolocation","data","basin","timestamp", "data_keys", "units", "source", "station", "cast"],
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
        "data_warning": {
            "bsonType": "array",
            "items": {
                "bsonType": "string",
                "enum": ["degenerate_levels", "missing_basin", "missing_location", "missing_timestamp"]
            }
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
        "station": {
            "bsonType": "int"
        },
        "cast": {
            "bsonType": "int"
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

db.command('collMod','goshipMeta', validator={"$jsonSchema": goshipmetaSchema}, validationLevel='strict')
db['goshipMeta'].create_index([("woce_lines", 1)])
db['goshipMeta'].create_index([("cchdo_cruise_id", 1)])

db.command('collMod','goship', validator={"$jsonSchema": goshipSchema}, validationLevel='strict')
db['goship'].create_index([("metadata", 1)])
db['goship'].create_index([("timestamp", -1), ("geolocation", "2dsphere")])
db['goship'].create_index([("geolocation", "2dsphere")])
