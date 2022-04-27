# db-schema

This repo contains scripts to create fresh collections in mongodb, including schema enforcement for the documents that are meant to reside there. *These schema are the sole and determining source of truth for the correct format for documents in these collections*. Any conflicts with other schema docs or specifications are to be settled in favor of what's recorded here.

## Oceanic Profiles

 - script: `pointSchema.py`
 - collection: `profiles` and `tc`
 - contents: Argo and GO-SHIP profiles, tropical cyclones.

## Gridded Products

 - script: `grids.py`, `grids-meta.py`
 - collection: `grids-meta` for all grid metadata; each grid has its own collection.
 - contents: currently the RG total temperature and salinity grids, and an OHC grid.
