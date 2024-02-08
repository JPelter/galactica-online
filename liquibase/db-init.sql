--DEV INIT
CREATE LOGIN galactica_dev WITH password='';

CREATE USER galactica_dev FROM LOGIN galactica_dev;

-- Create schema
CREATE SCHEMA galactica_dev AUTHORIZATION galactica_dev;

ALTER USER galactica_dev WITH DEFAULT_SCHEMA = galactica_dev;

-- Grant CREATE TABLE permission
GRANT CREATE TABLE TO galactica_dev;

-- Grant ALTER permission for schema changes
GRANT ALTER ON SCHEMA::galactica_dev TO galactica_dev;

--PROD INIT
CREATE LOGIN galactica WITH password='';

CREATE USER galactica FROM LOGIN galactica;

-- Create schema
CREATE SCHEMA galactica AUTHORIZATION galactica;

ALTER USER galactica WITH DEFAULT_SCHEMA = galactica;

-- Grant CREATE TABLE permission
GRANT CREATE TABLE TO galactica;

-- Grant ALTER permission for schema changes
GRANT ALTER ON SCHEMA::galactica TO galactica;