# usage: python drifters.py
# creates empty collections in the argo db called drifterMeta and drifters with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

db['drifterMeta'].drop()
db.create_collection('drifterMeta')
db['drifter'].drop()
db.create_collection('drifter')

driftermetaSchema = {
    "bsonType": "object",
    "required": ["_id", "rowsize", "wmo", "expno", "deploy_date", "deploy_lon", "deploy_lat", "end_date", "end_lon", "end_lat", "drogue_lost_date", "typedeath", "typebuoy", "data_type", "date_updated_argovis", "source", "data_keys", "units", "long_name", "platform"],
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
                "bsonType": "string",
                "enum": ["ve","vn","err_lon","err_lat","err_ve","err_vn","gap","sst","sst1","sst2","err_sst","err_sst1","err_sst2","flg_sst","flg_sst1","flg_sst2"]
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
        "platform": {
            "bsonType": "string"
        },
        "rowsize": {
            "bsonType": "int"
        },
        "wmo": {
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
    "required": ["_id","metadata","geolocation","data","basin","timestamp"],
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
        }
    }
}

db.command('collMod','drifterMeta', validator={"$jsonSchema": driftermetaSchema}, validationLevel='strict')
db['drifterMeta'].create_index([("wmo", 1)])
db['drifterMeta'].create_index([("platform", 1)])

db.command('collMod','drifter', validator={"$jsonSchema": drifterSchema}, validationLevel='strict')
db['drifter'].create_index([("metadata", 1)])
db['drifter'].create_index([("timestamp", -1), ("geolocation", "2dsphere")])
db['drifter'].create_index([("geolocation", "2dsphere")])
