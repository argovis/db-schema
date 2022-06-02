# usage: python drifters.py
# creates empty, unindexed collections in the argo db called drifterMeta and drifters with schema validation enforcement

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

db['drifterMetax'].drop()
db.create_collection('drifterMetax')
db['driftersx'].drop()
db.create_collection('driftersx')

driftermetaSchema = {
    "bsonType": "object",
    "required": ["_id", "rowsize", "WMO", "expno", "deploy_date", "deploy_lon", "deploy_lat", "end_date", "end_lon", "end_lat", "drogue_lost_date", "typedeath", "typebuoy", "data_type", "date_updated_argovis", "source_info", "data_keys", "units", "long_name"],
    "properties":{
        "_id": {
            "bsonType": "string"
        },
        "rowsize": {
            "bsonType": "int"
        },
        "WMO": {
            "bsonType": "int"
        },
        "expno": {
            "bsonType": "int"
        },
        "deploy_date": {
            "bsonType": ["date", "null"]
        },
        "deploy_lon": {
            "bsonType": "double"
        },
        "deploy_lat": {
            "bsonType": "double"
        },
        "end_date": {
            "bsonType": ["date", "null"]
        },
        "end_lon": {
            "bsonType": "double"
        },
        "end_lat": {
            "bsonType": "double"
        },
        "drogue_lost_date": {
            "bsonType": ["date", "null"]
        },
        "typedeath": {
            "bsonType": "int"
        },
        "typebuoy": {
            "bsonType": "string"
        },
        "data_type": {
            "bsonType": "string"
        },
        "date_updated_argovis": {
            "bsonType": "date"
        },
        "source_info": {
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
                    "source_url": {
                        "bsonType": "string",
                    }
                }
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
        "long_name": {
            "bsonType": "array",
            "items": {
                "bsonType": ["string", "null"]
            }
        }
    }
}

drifterSchema = {
    "bsonType": "object",
    "required": ["platform","geolocation","data","basin","timestamp"],
    "properties": {
        "_id": {
            "bsonType": "string"
        },
        "platform": {
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
        "data": {
            "bsonType": "array",
            "items": {
                "bsonType": "array",
                "items": {
                    "bsonType": ["double", "int"]
                }
            }
        },
        "basin": {
            "bsonType": "int"
        },
        "timestamp": {
            "bsonType": ["date", "null"]
        }
    }
}

db.command('collMod','drifterMetax', validator={"$jsonSchema": driftermetaSchema}, validationLevel='strict')
db.command('collMod','driftersx', validator={"$jsonSchema": drifterSchema}, validationLevel='strict')
