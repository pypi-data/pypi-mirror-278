# SCUAMATE
### '**S**ome **C**loud **U**tilities to **A**dvance **M**onitoring of **A**nimals and **T**heir **E**cosystems' (or, '**S**ome **C**loud **U**tilities for **A**nimals, **MATE**')

A Python package containing utilities to help run, maintain, check, and back
up the cloud infrastructure for next-generation wildlife monitoring projects
(originally developed at CSIRO for SpaceCows and the National Koala Monitoring Program)

##### Contents:
- **scuamate**: a variety of general-purpose classes and functions
- **scuamate.az**: functions for working with Azure services, including:
  - **scauamate.az.keyvault**: for pulling secrets from an Azure KeyVault
  - **scauamate.az.mssql**: for connecting to, pulling data from, pushing data to, and editing data in an MSSQL database
  - **scauamate.az.azfuncs**: for working with Azure functions 
- **scuamate.gc**: functions for working with Google Cloud services, including:
  - **scuamate.gc.firestore**: functions for running CRUD operations on a Firestore database
- **scuamate.gsattrack**: functions for authenticating with and getting data from the GSatTrack API

