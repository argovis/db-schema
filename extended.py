# usage: python extended.py <collection name, like 'ar'>
# creates empty collections in the argo db called <collection name>Meta and <collection name> with schema validation enforcement and defined indexes
# appropriate for extended object collections

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

extendedMetaSchema = {
    "bsonType": "object",
    "required": ['_id', 'data_type', 'data_info', 'date_updated_argovis', 'source'],
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
        }
    }
}

extendedSchema = {
    "bsonType": "object",
    "required": ['_id', "geolocation", "timestamp", "raster"],
    "properties": {
        "_id": {
            "bsonType": "string"
        },
        "geolocation": geolocation,
        "timestamp": timestamp,
        "raster": {
            # nominally [ [lon1, lat1, [scalars]], [lon2, lat2, [scalars]], ...]
            "bsonType": "array",
            "items": {
                "bsonType": "array",
                "items": {
                    "bsonType": ["double", "int", "array"]
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

db.command('collMod',metacollection, validator={"$jsonSchema": extendedMetaSchema}, validationLevel='strict')

db.command('collMod',datacollection, validator={"$jsonSchema": extendedSchema}, validationLevel='strict')
db[datacollection].create_index([("metadata", 1)])
db[datacollection].create_index([("timestamp", -1)])
db[datacollection].create_index([("geolocation", "2dsphere")])