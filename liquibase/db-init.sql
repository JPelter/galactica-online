--DEV INIT
CREATE LOGIN galactica_dev WITH password='';

CREATE USER galactica_dev FROM LOGIN galactica_dev;

-- Create schema
CREATE SCHEMA galactica_dev AUTHORIZATION galactica_dev;

ALTER USER galactica_dev WITH DEFAULT_SCHEMA = galactica_dev;

-- Grant CREATE TABLE permission
GRANT CREATE TABLE TO galactica_dev;

--PROD INIT
CREATE LOGIN galactica WITH password='';

CREATE USER galactica FROM LOGIN galactica;

-- Create schema
CREATE SCHEMA galactica AUTHORIZATION galactica;

ALTER USER galactica WITH DEFAULT_SCHEMA = galactica;

-- Grant CREATE TABLE permission
GRANT CREATE TABLE TO galactica;

-- HELPQUL QUERIES!
SELECT * FROM galactica_dev.DATABASECHANGELOG
SELECT * FROM galactica_dev.AGENT
INSERT INTO galactica_dev.AGENT ([name], crypto, controller_email) VALUES ('Publius', 0, 'jake.pelter@gmail.com')
INSERT INTO galactica_dev.AGENT ([name], crypto, controller_email) VALUES ('Brutus', 0, 'jake.pelter@gmail.com')