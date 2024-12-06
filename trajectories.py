# usage: python trajectories.py
# creates empty collections in the argo db called trajectoriesMeta and trajectories with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

metacollection = 'trajectoriesMetax'
datacollection = 'trajectoriesx'

db[metacollection].drop()
db.create_collection(metacollection)
db[datacollection].drop()
db.create_collection(datacollection)

geolocation = {
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
}

timestamp = {
    "bsonType": ["date", "null"]
}

trajectoriesMetaSchema = {
    "bsonType": "object",
    "required": ['_id', 'data_type', 'data_info', 'date_updated_argovis', 'source', 'platform', 'positioning_system_flag', 'sensor_type_flag', 'mission_flag', 'extrapolation_flag', 'platform_type'],
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
        "platform": {
            "bsonType": "string"
        },
        "positioning_system_flag": {
            "bsonType": ["double", "int", "null"]
        },
        "sensor_type_flag": {
            "bsonType": ["double", "int", "null"]
        },
        "mission_flag": {
            "bsonType": ["double", "int", "null"]
        },
        "extrapolation_flag": {
            "bsonType": ["double", "int", "null"]
        },
        "positioning_system": {
            "bsonType": "string"
        },
        "platform_type": {
            "bsonType": "string"
        }
    }
}

trajectoriesSchema = {
    "bsonType": "object",
    "required": ['_id', "cycle_number", "geolocation", "geolocation_descending", "geolocation_ascending", "geolocation_descending_transmitted", "geolocation_ascending_transmitted", "geolocation_midpoint_transmitted", "timestamp", "timestamp_descending", "timestamp_ascending", "timestamp_descending_transmitted", "timestamp_ascending_transmitted", "timestamp_midpoint_transmitted", "data"],
    "properties": {
        "_id": {
            "bsonType": "string"
        },
        "cycle_number": {
            "bsonType": ["double", "int", "null"]
        },
        "geolocation": geolocation,
        "geolocation_descending": geolocation,
        "geolocation_ascending": geolocation,
        "geolocation_descending_transmitted": geolocation,
        "geolocation_ascending_transmitted": geolocation,
        "geolocation_midpoint_transmitted": geolocation,
        "timestamp": timestamp,
        "timestamp_descending": timestamp,
        "timestamp_ascending": timestamp,
        "timestamp_descending_transmitted": timestamp,
        "timestamp_ascending_transmitted": timestamp,
        "timestamp_midpoint_transmitted": timestamp,
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

db.command('collMod',metacollection, validator={"$jsonSchema": trajectoriesMetaSchema}, validationLevel='strict')
db[metacollection].create_index([("platform", 1)])

db.command('collMod',datacollection, validator={"$jsonSchema": trajectoriesSchema}, validationLevel='strict')
db[datacollection].create_index([("metadata", 1)])
db[datacollection].create_index([("timestamp", -1), ("geolocation", "2dsphere")])
db[datacollection].create_index([("timestamp", -1)])
db[datacollection].create_index([("geolocation", "2dsphere")])
db[datacollection].create_index([("geolocation.coordinates", "2d"), ("timestamp", -1)])