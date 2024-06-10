# lapa_file_store

## about

file storage layer for my personal server.

## installation

> pip install lapa_file_store

## configs

1. lapa_file_store\data\config.ini
2. square_logger\data\config.ini

## env

- python>=3.12.0

## changelog

### v0.0.12

- Added test cases.Updated

### v0.0.11

- add SQUARE_LOGGER and LAPA_DATABASE_HELPER sections in config and initialise sdks using these variables.
- update min version of lapa_commons.
- keep square_logger and lapa_database_structure as >= instead of ~=.

### v0.0.10

- Bug fix /delete_file endpoint because of input list as query param.

### v0.0.9

- Added /delete_file endpoint.

### v0.0.8

- update import logic from lapa_database_structure.

### v0.0.7

- bug fix in utils->Helper.py import.

### v0.0.6

- read database configuration from config using enums from lapa database structure.

### v0.0.5

- use lapa_commons to read config.

### v0.0.4

- Bug Fix in /download_file because of ignore_filters_and_get_all.

### v0.0.3

- MODULE_NAME added in the GENERAL configuration.
- / root endpoint added.
- Form data and description added for /upload_file endpoint for the below params.
  - file_purpose
  - system_relative_path
- Validation added while creating the directory in /upload_file endpoint.
- /download_file endpoint changed from POST to GET.

### v0.0.2

- change default port to 10100.
- change default LOCAL_STORAGE_PATH to be relative and LOCAL_STORAGE_PATH.
- move logger to configuration.py.
- fix dependencies in setup.py.
- minor optimisations.
- add validation for LOCAL_STORAGE_PATH in config.ini.
- fix logic for upload_file.
- fix logic for download_file.

### v0.0.1

- Base version
