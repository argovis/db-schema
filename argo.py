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

argo_measurements = ["bbp470","bbp532","bbp700","bbp700_2","bisulfide","cdom","chla","cndc","cndx","cp660","down_irradiance380","down_irradiance412","down_irradiance442","down_irradiance443","down_irradiance490","down_irradiance555","down_irradiance670","downwelling_par","doxy","doxy2","doxy3","molar_doxy","nitrate","ph_in_situ_total","pressure","salinity","salinity_sfile","temperature","temperature_sfile","turbidity","up_radiance412","up_radiance443","up_radiance490","up_radiance555","bbp470_argoqc","bbp532_argoqc","bbp700_argoqc","bbp700_2_argoqc","bisulfide_argoqc","cdom_argoqc","chla_argoqc","cndc_argoqc","cndx_argoqc","cp660_argoqc","down_irradiance380_argoqc","down_irradiance412_argoqc","down_irradiance442_argoqc","down_irradiance443_argoqc","down_irradiance490_argoqc","down_irradiance555_argoqc","down_irradiance670_argoqc","downwelling_par_argoqc","doxy_argoqc","doxy2_argoqc","doxy3_argoqc","molar_doxy_argoqc","nitrate_argoqc","ph_in_situ_total_argoqc","pressure_argoqc","salinity_argoqc","salinity_sfile_argoqc","temperature_argoqc","temperature_sfile_argoqc","turbidity_argoqc","up_radiance412_argoqc","up_radiance443_argoqc","up_radiance490_argoqc","up_radiance555_argoqc"]

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
                "bsonType": "string",
                "enum": argo_measurements
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
                "bsonType": "string",
                "enum": argo_measurements
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
db['argoMeta'].create_index([("data_center", 1)])
db['argoMeta'].create_index([("platform", 1)])

db.command('collMod','argo', validator={"$jsonSchema": argoSchema}, validationLevel='strict')
db['argo'].create_index([("metadata", 1)])
db['argo'].create_index([("timestamp", -1), ("geolocation", "2dsphere")])
db['argo'].create_index([("geolocation", "2dsphere")])
db['argo'].create_index([("source.source", 1)])
