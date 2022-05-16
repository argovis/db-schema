# usage: python drifterMeta.py
# creates an empty, unindexed collection in the argo db called drifterMeta with schema validation enforcement

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

db['drifterMeta'].drop()
db.create_collection('drifterMeta')

driftermetaSchema = {
    "bsonType": "object",
    "required": ["_id", "rowsize", "WMO", "expno", "deploy_date", "deploy_lon", "deploy_lat", "end_date", "end_lon", "end_lat", "drogue_lost_date", "typedeath", "typebuoy"],
    "properties":{
        "_id": {
            "bsonType": "string"
        },
        "rowsize": {
            "bsonType": "int"
        },
        "WMO": {
            "bsonType": "double"
        },
        "expno": {
            "bsonType": "double"
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
            "bsonType": "double"
        },
        "typebuoy": {
            "bsonType": "string"
        }
    }
}

db.command('collMod','drifterMeta', validator={"$jsonSchema": driftermetaSchema}, validationLevel='strict')

