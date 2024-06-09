# lapa_database_structure

## about

database structure layer for my personal server.

## installation

> pip install lapa_database_structure

## usage

### to add a new database

- create a package with package name as database name.

### to add a new schema

- add package in database_name package with schema name as package name.

### to add a new table

- create /database_name/schema_name/tables.py file if not already created.
- create class corresponding to your new table add in /database_name/schema_name/tables.py file.

### to add default data in table

- append row objects containing your default data to the data_to_insert list inside the
  /database_name/schema_name/tables.py file.

**do not forget to add new database_names, schema_names and/or table_names to main.py enums to make it accessible
through api calls.**

**do not forget to clone changes to all testing database.**

## configs

None

## env

- python>=3.12.0

## changelog

### v0.0.15

lapa and lapa_testing

- authentication
    - rename user_session_hashed_refresh_token to user_session_refresh_token

### v0.0.14

lapa and lapa_testing

- authentication
    - remove device table and remove references of device in user_device_session (old name).
    - add session_expiry_time in user_session table.
- public
    - add table for testing.

### v0.0.13

lapa and lapa_testing

- authentication
    - naming convention changes to tables and columns.
    - make user_id unique in user_credential table. (1 user can have only 1 username-password)
    - make user_id unique in user_profile table. (1 user can have only 1 profile)
    - add auto increment to user_log_id and user_device_session_id. (primary keys)
    - introduce device_id in device table.
    - assign foreign key to user_id in user_device_session table.
    - introduce foreign key device_id to user_device_session table.
    - make device_encrypted_mac_address unique in device table. (unencrypted mac address is supposed to be unique)
    - make user_device_session_hashed_refresh_token unique in device table. (plaintext refresh token is supposed to be
      unique)

### v0.0.12

- removed UserAuthentication
- renamed user_authentication -> credential
- new table device and user_device_session

### v0.0.11

- removed salt authentication_username_salt column

### v0.0.10

- renamed authentication_username_salt.
- added local_string_database_name in each database.
- removed main.py file and its enums.

### v0.0.9

- rename authentication_username_hashed_access_token and authentication_username_hashed_refresh_token.
- update enum in main.py.

### v0.0.8

- Overhauled authentication schema, again.

### v0.0.7

- Overhauled authentication schema,
- introducing new tables: User, UsernameAuthentication, UserProfile, AuthenticationType, UserAccountStatus, UserLog, and
  UserLogStatus.

### v0.0.6

- changed db structure
- removed game db
- added testing db which is clone of lapa

### v0.0.5

- file_storage -> public -> File
    - change file_extension to file_content_type.
    - file_system_relative_path default change from "." to "".

### v0.0.4

- authentication database added with the below tables
    - user
    - user_validation_status
    - user_registration
    - hashing_algorithm

### v0.0.3

- Changed package name to lapa_database_structure.

### v0.0.2

- Update table for file_storage -> File.

### v0.0.1

- initial implementation.

## Feedback is appreciated. Thank you!
