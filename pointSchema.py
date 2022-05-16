# usage: python pointSchema.py
# creates an empty, unindexed collection in the argo db with schema validation enforcement
# permits argo or goship-flavored profiles in `profiles`.

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

#db.profilesx.drop()
#db.create_collection("profilesx")

db.drifters.drop()
db.create_collection("drifters")

def combineSchema(parent, ext):
    # combine a parent and an extension dict into a single dict
    # ext keys clobber collisions, with the exception of "required", which should be merged.

    required = []
    required.extend(parent['required'])
    required.extend(ext['required'])
    schema = {"bsonType": "object"}
    schema['properties'] = {**parent['properties'], **ext['properties']}
    schema['dependencies'] = {**parent['dependencies'], **ext['dependencies']}
    schema['required'] = required
    return schema 

pointSchema = {
  "bsonType": "object",
  "required": ["_id", "basin", "data_type", "geolocation", "timestamp", "date_updated_argovis", "source_info"],
  "properties": {
    "_id": {
        "bsonType": "string"
    },
    "basin": {
        "bsonType": "int"
    },
    "data_type": {
        "bsonType": "string"
    },
    "data_warning": {
        "bsonType": "array",
        "items": {
            "bsonType": "string"
        }
    },
    "doi": {
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
    "instrument": {
        "bsonType": "string"
    },
    "data": {
        "bsonType": "array",
        "items": {
            "bsonType": "array"
        }
    },
    "data_keys": {
        "bsonType": "array",
        "items": {
            "bsonType": "string"
        }
    },
    "timestamp": {
        "bsonType": "date"
    },
    "date_updated_argovis": {
        "bsonType": "date"
    },
    "pi_name": {
        "bsonType": "array",
        "items": {
            "bsonType": "string"
        }
    },
    "platform_id": {
        "bsonType": "string"
    },
    "platform_type": {
        "bsonType": "string"
    },
    "country": {
        "bsonType": "string"
    },
    "data_center": {
        "bsonType": "string"
    },
    "source_info": {
        "bsonType": "array",
        "items": {
            "bsonType": "object",
            "required": ["source"],
            "properties": {
                "data_keys_source": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "string"
                    }
                },
                "source": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "string"
                    }
                },
                "source_url": {
                    "bsonType": "string",
                },
                "date_updated_source": {
                    "bsonType": "date",
                }
            }
        }
    }
  },
  "dependencies": {
    "data": ["data_keys"]
  }
}

argoSchemaExtension = {
  "bsonType": "object",
  "required": ["cycle_number"],
  "properties": {
    "profile_direction": {
        "bsonType": "string"
    },
    "geolocation_argoqc": {
        "bsonType": "int"
    },
    "timestamp_argoqc": {
        "bsonType": "int"
    },
    "cycle_number": {
        "bsonType": "int"
    },
    "fleetmonitoring": {
        "bsonType": "string"
    },
    "oceanops": {
        "bsonType": "string"
    },
    "data_keys_mode": {
        "bsonType": "object"    
    },
    "positioning_system": {
        "bsonType": "string"
    },
    "vertical_sampling_scheme": {
        "bsonType": "string"
    },
    "wmo_inst_type": {
        "bsonType": "string"
    }
  },
  "dependencies": {}
}

goshipSchemaExtension = {
    "bsonType": "object",
    "required": ['expocode'],
    "properties": {
        "expocode": {"bsonType": "string"},
        "woce_lines": {
            "bsonType": "array",
            "items": {
                "bsonType": "string"
            }
        },
        "cchdo_cruise_id": {"bsonType": "int"},
        "cast": {"bsonType": "int"},
        "station": {"bsonType": "string"}
    },
    "dependencies": {}
}

tropicalCycloneSchemaExtension = {
    "bsonType": "object",
    "required": [],
    "properties": {
        "name": {"bsonType": "string"},
        "record_identifier": {"bsonType": "string"},
        "class": {"bsonType": "string"},
        "num": {"bsonType": "int"}
    },
    "dependencies": {}
}

argoProfile = combineSchema(pointSchema, argoSchemaExtension)
goshipProfile = combineSchema(pointSchema, goshipSchemaExtension)
tropicalCyclone = combineSchema(pointSchema, tropicalCycloneSchemaExtension)

#db.command('collMod','profiles', validator={"$jsonSchema": {"oneOf": [argoProfile, goshipProfile]}}, validationLevel='strict')
#db.command('collMod','tc', validator={"$jsonSchema": tropicalCyclone}, validationLevel='strict')
db.command('collMod','drifters', validator={"$jsonSchema": pointSchema}, validationLevel='strict') # no drifter schema extension; drifter-specific data is all in drifterMeta
