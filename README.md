# db-schema

This repo contains scripts to create fresh collections in mongodb, including schema enforcement for the documents that are meant to reside there. *These schema are the sole and determining source of truth for the correct format for documents in these collections*. Any conflicts with other schema docs or specifications are to be settled in favor of what's recorded here.

## Re-creating all collections from scratch

In the event that you're populating a new MongoDB instance, start by building the image defined by the local `Dockerfile`, and running it on Kube per `pod.yaml`, or as an interactive container. From a command line inside the container:

```
python argo.py
python cchdo.py
python drifters.py
python grids-meta.py
python grids.py temperature_rg
python grids.py salinity_rg
python grids.py ohc_kg
python tc.py
```

If all is well, you should have empty collections for all datasets and their metadata, with schema and indexes defined.