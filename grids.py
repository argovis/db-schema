# usage: python grids.py <grid name>
# creates an empty, unindexed collection in the argo db called <grid name> with schema validation enforcement

from pymongo import MongoClient
import sys

grid = sys.argv[1]
client = MongoClient('mongodb://database/argo')
db = client.argo

db[grid].drop()
db.create_collection(grid)

gridSchema = {
    "bsonType": "object",
    "required": ["g","t","d"],
    "properties":{
        "g": {
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
        "t": {
            "bsonType": "date"
        },
        "d": {
            "bsonType": "array",
            "items": {
                "bsonType": ["double", "int"]
            }
        }
    }
}

db.command('collMod',grid, validator={"$jsonSchema": gridSchema}, validationLevel='strict')

