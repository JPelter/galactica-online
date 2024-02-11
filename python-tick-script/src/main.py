# STL

# STL
import logging
from os import environ
from time import sleep


logging.basicConfig(level=getattr(logging, environ.get("LOGGING_LEVEL", "INFO")))

# EXT
from sqlalchemy import and_, asc, create_engine, inspect, or_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

# AUTH
logging.info(f"Creating database connection and objects!")
db_engine = create_engine(f"mssql+pyodbc://{environ['SQL_SERVER_USERNAME']}:{environ['SQL_SERVER_PASSWORD']}@{environ['SQL_SERVER_HOST']}/{environ['SQL_SERVER_DB']}?driver=ODBC+Driver+17+for+SQL+Server")
db_Base = automap_base()
db_Base.prepare(db_engine)

AGENT = db_Base.classes.AGENT
BUILDING = db_Base.classes.BUILDING
BUILDING_RESOURCE_NET_MAINTENANCE_COST = db_Base.classes.BUILDING_RESOURCE_NET_MAINTENANCE_COST
BUILDING_TYPE = db_Base.classes.BUILDING_TYPE
RESOURCE = db_Base.classes.RESOURCE
SHIP = db_Base.classes.SHIP
SHIP_CARGO = db_Base.classes.SHIP_CARGO
SHIP_RESOURCE_NET_MAINTENANCE_COST = db_Base.classes.SHIP_RESOURCE_NET_MAINTENANCE_COST
SHIP_TYPE = db_Base.classes.SHIP_TYPE
SYSTEM = db_Base.classes.SYSTEM
SYSTEM_RESOURCE_STOCKPILE = db_Base.classes.SYSTEM_RESOURCE_STOCKPILE

session = Session(db_engine)

if __name__ == '__main__':
    logging.info("Starting tick script loop!")
    while True:
        logging.info("Top of the loop!")
        systems = session.query(SYSTEM).all()
        if systems:
            logging.info(f"Found {len(systems)} systems!")
        agents = session.query(AGENT).all()
        if agents:
            logging.info(f"Found {len(agents)} agents!")
        sleep(30)