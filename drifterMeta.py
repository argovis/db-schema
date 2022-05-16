# usage: python drifterMeta.py
# creates an empty, unindexed collection in the argo db called drifterMeta with schema validation enforcement

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

db['drifterMeta'].drop()
db.create_collection('drifterMeta')


    "_id": ds.ID.data[0].decode("utf-8").strip(), 
    "rowsize": ds.rowsize.data[0],
    "WMO": ds.WMO.data[0],
    "expno": ds.expno.data[0],
    "deploy_date": datetime.datetime.fromtimestamp(int(ds.deploy_date.data[0]), datetime.timezone.utc),
    "deploy_lon": ds.deploy_lon.data[0],
    "deploy_lat": ds.deploy_lat.data[0],
    "end_date": datetime.datetime.fromtimestamp(int(ds.end_date.data[0]), datetime.timezone.utc),
    "end_lon": ds.end_lon.data[0],
    "end_lat": ds.end_lat.data[0],
    "drogue_lost_date": datetime.datetime.fromtimestamp(int(ds.drogue_lost_date.data[0]), datetime.timezone.utc),
    "typedeath": ds.typedeath.data[0],
    "typebuoy": ds.typebuoy.data[0].decode("utf-8").strip()

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

