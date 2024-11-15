# usage: python easyocean.py
# creates empty collections in the argo db called easyoceanMeta and easyocean with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

metacollection = 'easyoceanMeta'
datacollection = 'easyocean'

db[metacollection].drop()
db.create_collection(metacollection)
db[datacollection].drop()
db.create_collection(datacollection)

easyoceanmetaSchema = {
    "bsonType": "object",
    "required": ["_id","occupancies","date_updated_argovis","data_type"],
    "properties": {
        "_id": {
            "bsonType": "string"
        },
        "data_type": {
            "bsonType": "string"
        },
        "occupancies": {
            "bsonType": "array",
            "items": {
                "bsonType": "object",
                "required": ["varying_direction", "static_direction", "expocodes", "time_boundaries"],
                "properties": {
                    "varying_direction": {
                        "bsonType": "string"
                    },
                    "static_direction": {
                        "bsonType": "string"
                    },
                    "expocodes": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "string"
                        }
                    },
                    "time_boundaries": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "date"
                        }
                    }
                }
            }
        },
        "date_updated_argovis": {
            "bsonType": "date"
        }
    }
}

easyoceanSchema = {
    "bsonType": "object",
    "required": ["_id","metadata","geolocation","data","basin","timestamp","data_info","source"],
    "properties":{
        "_id": {
            "bsonType": "string"
        },
        "metadata": {
            "bsonType": "array",
            "items": {
                "bsonType": "string"
            }
        },
        "section_expocodes": {
            "bsonType": "array",
            "items": {
                "bsonType": "string"
            }            
        },
        "section_start_date": {
            "bsonType": "date"
        },
        "section_end_date": {
            "bsonType": "date"
        },
        "woce_lines": {
            "bsonType": "array",
            "items": {
                "bsonType": "string"
            }
        },
        "instrument": {
            "bsonType": "string"
        },
        "references": {
            "bsonType": "string"
        },
        "dataset_created": {
            "bsonType": "date"
        },
        "section_countries": {
            "bsonType": "array",
            "items": {
                "bsonType": "string"
            }
        },
        "positioning_system": {
            "bsonType": "string"
        },
        "data_center": {
            "bsonType": "string"
        },
        "source": {
            "bsonType": "array",
            "items": {
                "bsonType": "object",
                "required": ["source", "url"],
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
                    "filename": {
                        "bsonType": "string",
                    }
                }
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



db.command('collMod',metacollection, validator={"$jsonSchema": easyoceanmetaSchema}, validationLevel='strict')

db.command('collMod',datacollection, validator={"$jsonSchema": easyoceanSchema}, validationLevel='strict')
db[datacollection].create_index([("metadata", 1)])
db[datacollection].create_index([("timestamp", -1), ("geolocation", "2dsphere")])
db[datacollection].create_index([("timestamp", -1)])
db[datacollection].create_index([("geolocation", "2dsphere")])
db[datacollection].create_index([("woce_lines", -1), ("section_start_date", -1)])
db[datacollection].create_index([("geolocation.coordinates", "2d"), ("timestamp", -1)])

