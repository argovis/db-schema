# usage: python argo.py
# creates empty collections in the argo db called argoMeta and argo with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

metacollection = 'covarianceMeta'
datacollection = 'covariance'

db[metacollection].drop()
db.create_collection(metacollection)
db[datacollection].drop()
db.create_collection(datacollection)

covarianceMetaSchema = {
    "bsonType": "object",
    "required": ["_id", "data_type", "data_keys", "units", "date_updated_argovis", "source", "levels"],
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
                "properties": {                    
                    "doi": {
                        "bsonType": "string",
                    }
                }
            }
        },
        "levels": {
            "bsonType": "array",
            "items": {
                "bsonType": ["int"]
            }      
        }
       
    }
}

covarianceSchema = {
    "bsonType": "object",
    "required": ["_id","metadata","geolocation","geolocation_forecast","data"],
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
        "geolocation_forecast": {
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
                    "bsonType": ["double", "int", "string", "null"]
                }
            }
        }
    }
}

db.command('collMod',metacollection, validator={"$jsonSchema": covarianceMetaSchema}, validationLevel='strict')

db.command('collMod',datacollection, validator={"$jsonSchema": covarianceSchema}, validationLevel='strict')
db[datacollection].create_index([("geolocation", "2dsphere")])
db[datacollection].create_index([("geolocation_forecast", "2dsphere")])
