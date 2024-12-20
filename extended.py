# generic extended object schema
# usage: for a new dataset: python extended.py [series data collection name, like 'ar']
# to recreate the shared meta collection: python extended.py meta
# creates empty collections in the argo db with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

geolocation = {
    "bsonType": "object",
    "required": ["type", "coordinates"],
    "properties": {
        "type":{
            "enum": ["MultiPolygon"]
        },
        "coordinates":{
            "bsonType": "array",
            "items": {
                "bsonType": "array",
                "items": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "array",
                        "minItems": 2,
                        "maxItems": 2,
                        "items": {
                            "bsonType": ["double", "int"]
                        }
                    }
                }
            }
        }
    }
}

timestamp = {
    "bsonType": ["date", "null"]
}

if sys.argv[1] == 'meta':
    metacollection = 'extendedMeta'
    db[metacollection].drop()
    db.create_collection(metacollection)

    extendedMetaSchema = {
        "bsonType": "object",
        "required": ['_id', 'data_type', 'data_info', 'date_updated_argovis', 'source', 'lattice'],
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
            "lattice": {
                "bsonType": "object",
                "required": ["center", "spacing", "minLat", "minLon", "maxLat", "maxLon"],
                "properties": {
                    "center": {
                        "bsonType": "array",
                        "minItems": 2,
                        "maxItems": 2,
                        "items": {
                            "bsonType": ["double", "int"]
                        }
                    },
                    "spacing": {
                        "bsonType": "array",
                        "minItems": 2,
                        "maxItems": 2,
                        "items": {
                            "bsonType": ["double", "int"]
                        }
                    },
                    "minLat": {
                        "bsonType": ["double", "int"]
                    },
                    "minLon": {
                        "bsonType": ["double", "int"]
                    },
                    "maxLat": {
                        "bsonType": ["double", "int"]
                    },
                    "maxLon": {
                        "bsonType": ["double", "int"]
                    }
                }
            }
        }
    }

    db.command('collMod',metacollection, validator={"$jsonSchema": extendedMetaSchema}, validationLevel='strict')
else:

    datacollection = sys.argv[1]
    db[datacollection].drop()
    db.create_collection(datacollection)
    extendedSchema = {
        "bsonType": "object",
        "required": ['_id', 'metadata', "geolocation", "basins", "timestamp", "data"],
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
            "geolocation": geolocation,
            "basins": {
                "bsonType": "array",
                "items": {
                    "bsonType": ["int"]
                }
            },
            "timestamp": timestamp,
            "data": {
                "bsonType": "array",
                "items": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": ["double", "int", "string", "null"]
                    }
                }
            },
            "true_geolocation": geolocation,
            "flags": {
                "bsonType": "array",
                "items": {
                    "bsonType": ["string"]
                }
            }
        }
    }

    db.command('collMod',datacollection, validator={"$jsonSchema": extendedSchema}, validationLevel='strict')
    db[datacollection].create_index([("metadata", 1)])
    db[datacollection].create_index([("timestamp", -1)])
    db[datacollection].create_index([("geolocation", "2dsphere")])