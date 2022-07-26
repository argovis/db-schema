# usage: python argo.py
# creates empty collections in the argo db called argoMeta and argo with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

db['argoMeta'].drop()
db.create_collection('argoMeta')
db['argo'].drop()
db.create_collection('argo')

argoMetaSchema = {
    "bsonType": "object",
    "required": ["_id", "data_type"],
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

argoSchema = {
    "bsonType": "object",
    "required": ["_id","metadata","geolocation","basin","timestamp","data", "date_updated_argovis", "source", "cycle_number"],
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
                    "bsonType": ["double", "int", "string", "null"]
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
        "cycle_number": {
            "bsonType": "int"
        },
        "data_keys_mode": {
            "bsonType": "array",
            "items": {
                "bsonType": ["string", "null"]
            }
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
        "vertical_sampling_scheme": {
            "bsonType": "string"
        }
    }
}

db.command('collMod','argoMeta', validator={"$jsonSchema": argoMetaSchema}, validationLevel='strict')
db['argo'].create_index([("data_center", 1)])

db.command('collMod','argo', validator={"$jsonSchema": argoSchema}, validationLevel='strict')
db['argo'].create_index([("metadata", 1)])
db['argo'].create_index([("timestamp", -1), ("geolocation", "2dsphere")])
db['argo'].create_index([("geolocation", "2dsphere")])
db['argo'].create_index([("source.source", 1)])
