# usage: python cchdo.py
# creates empty collections in the argo db called cchdoMeta and cchdo with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

metacollection = 'cchdoMeta'
datacollection = 'cchdo'

db[metacollection].drop()
db.create_collection(metacollection)
db[datacollection].drop()
db.create_collection(datacollection)

cchdometaSchema = {
    "bsonType": "object",
    "required": ["_id", "date_updated_argovis", "data_type", "expocode", "cchdo_cruise_id", "woce_lines"],
    "properties":{
        "_id": {
            "bsonType": "string"
        },
        "date_updated_argovis": {
            "bsonType": "date"
        },
        "data_type": {
            "bsonType": "string"
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
        "expocode": {
            "bsonType": "string"
        },
        "cchdo_cruise_id": {
            "bsonType": ["double", "int"]
        },
        "woce_lines": {
            "bsonType": "array",
            "items": {
                "bsonType": "string"
            }
        }
    }
}

cchdoSchema = {
    "bsonType": "object",
    "required": ["_id","metadata","geolocation","data","basin","timestamp", "data_keys", "units", "source", "station", "cast"],
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
                "enum": ["ammonium_btl","ammonium_btl_woceqc","bionbr_btl","bottle_latitude_btl","bottle_longitude_btl","bottle_number_btl","bottle_number_btl_woceqc","bottle_salinity_btl","bottle_salinity_btl_woceqc","bottle_time_btl","carbon_tetrachloride_btl","carbon_tetrachloride_btl_woceqc","cfc_113_btl","cfc_113_btl_woceqc","cfc_11_btl","cfc_11_btl_woceqc","cfc_12_btl","cfc_12_btl_woceqc","chlorophyll_a_btl","chlorophyll_a_btl_woceqc","chlorophyll_a_ug_kg_btl","chlorophyll_a_ug_kg_btl_woceqc","co2_mole_fraction_btl","co2_mole_fraction_btl_woceqc","ctd_beamcp_ctd","ctd_beamcp_ctd_woceqc","ctd_beta700_raw_btl","ctd_beta700_raw_btl_woceqc","ctd_beta700_raw_ctd","ctd_beta700_raw_ctd_woceqc","ctd_cdom_raw_ctd","ctd_cdom_raw_ctd_woceqc","ctd_fluor_arbitrary_ctd","ctd_fluor_ctd","ctd_fluor_ctd_woceqc","ctd_fluor_raw_btl","ctd_fluor_raw_btl_woceqc","ctd_fluor_raw_ctd","ctd_fluor_raw_ctd_woceqc","ctd_nitrate_ctd","ctd_nitrate_ctd_woceqc","ctd_number_of_observations_ctd","ctd_optode_oxygen_ctd","ctd_optode_oxygen_ctd_woceqc","ctd_optode_oxygen_raw_ctd","ctd_optode_oxygen_raw_ctd_woceqc","ctd_pressure_raw_btl","ctd_temperature_unk_ctd","ctd_temperature_unk_ctd_woceqc","ctd_transmissometer_ctd","ctd_transmissometer_ctd_woceqc","ctd_transmissometer_raw_btl","ctd_transmissometer_raw_btl_woceqc","ctd_transmissometer_raw_ctd","ctd_transmissometer_raw_ctd_woceqc","ctd_turbidity_ntu_ctd","del_carbon_13_dic_btl","del_carbon_13_dic_btl_woceqc","del_carbon_14_dic_btl","del_carbon_14_dic_btl_woceqc","del_carbon_14_dic_error_btl","del_oxygen_18_btl","del_oxygen_18_btl_woceqc","del_oxygen_18_error_btl","delta_helium_3_btl","delta_helium_3_btl_woceqc","delta_helium_3_error_btl","dissolved_organic_carbon_btl","dissolved_organic_carbon_btl_woceqc","fm_depth_btl","fm_depth_ctd","fm_depth_ctd_woceqc","geotraces_sample_btl","helium_btl","helium_btl_woceqc","helium_error_btl","methyl_chloroform_btl","methyl_chloroform_btl_woceqc","neon_btl","neon_btl_woceqc","neon_error_btl","nitrate_btl","nitrate_btl_woceqc","nitrite_btl","nitrite_btl_woceqc","nitrite_nitrate_btl","nitrite_nitrate_btl_woceqc","nitrous_oxide_btl","nitrous_oxide_btl_woceqc","odf_pressure_btl","oxygen_btl","oxygen_btl_woceqc","oxygen_ctd","oxygen_ctd_woceqc","oxygen_ml_l_btl","oxygen_ml_l_btl_woceqc","package_depth_btl","par_ctd","par_ctd_woceqc","partial_co2_temperature_btl","partial_pressure_of_co2_btl","partial_pressure_of_co2_btl_woceqc","particulate_organic_carbon_btl","particulate_organic_carbon_btl_woceqc","particulate_organic_nitrogen_btl","particulate_organic_nitrogen_btl_woceqc","ph_sws_btl","ph_sws_btl_woceqc","ph_temperature_btl","ph_total_h_scale_btl","ph_total_h_scale_btl_woceqc","ph_unknown_scale_btl","ph_unknown_scale_btl_woceqc","phaeophytin_btl","phaeophytin_btl_woceqc","phaeophytin_ug_l_btl","phaeophytin_ug_l_btl_woceqc","phosphate_btl","phosphate_btl_woceqc","potential_temperature_68_btl","potential_temperature_c_btl","potential_temperature_c_ctd","pressure","pressure_btl_woceqc","pressure_ctd_woceqc","ref_temperature_btl","ref_temperature_btl_woceqc","ref_temperature_c_btl","ref_temperature_c_btl_woceqc","reference_salinity_btl","reference_salinity_btl_woceqc","rev_pressure_btl","rev_pressure_btl_woceqc","rev_temperature_90_btl","rev_temperature_90_btl_woceqc","rev_temperature_btl","rev_temperature_btl_woceqc","rev_temperature_c_btl","rev_temperature_c_btl_woceqc","salinity_btl","salinity_btl_woceqc","salinity_ctd","salinity_ctd_woceqc","sample_btl","sample_ctd","silicate_btl","silicate_btl_woceqc","sm_depth_btl","sm_depth_ctd","sm_depth_ctd_woceqc","sulfur_hexifluoride_btl","sulfur_hexifluoride_btl_woceqc","temperature_btl","temperature_btl_woceqc","temperature_ctd","temperature_ctd_woceqc","total_alkalinity_btl","total_alkalinity_btl_woceqc","total_carbon_btl","total_carbon_btl_woceqc","total_dissolved_nitrogen_btl","total_dissolved_nitrogen_btl_woceqc","total_organic_carbon_l_btl","total_organic_carbon_l_btl_woceqc","tritium_btl","tritium_btl_woceqc","tritium_error_btl","urea_btl","urea_btl_woceqc","user_bottle_number_btl","user_bottle_number_btl_woceqc","user_sample_number_btl"]
            }
        },
        "units": {
            "bsonType": "array",
            "items": {
                "bsonType": ["string", "null"]
            }
        },
        "station": {
            "bsonType": "string"
        },
        "cast": {
            "bsonType": "int"
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

db.command('collMod',metacollection, validator={"$jsonSchema": cchdometaSchema}, validationLevel='strict')
db[metacollection].create_index([("woce_lines", 1)])
db[metacollection].create_index([("cchdo_cruise_id", 1)])

db.command('collMod',datacollection, validator={"$jsonSchema": cchdoSchema}, validationLevel='strict')
db[datacollection].create_index([("metadata", 1)])
db[datacollection].create_index([("timestamp", -1), ("geolocation", "2dsphere")])
db[datacollection].create_index([("timestamp", -1)])
db[datacollection].create_index([("geolocation", "2dsphere")])
db[datacollection].create_index([("source.source", 1)])

