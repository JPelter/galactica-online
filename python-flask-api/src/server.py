# STL
from datetime import datetime, timedelta, timezone
from functools import wraps
import logging
from os import environ

# EXT
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from waitress import serve
from sqlalchemy.ext.automap import automap_base


from flask import Flask, session
############################
#### APP AND DB OBJECTS ####
############################
logging.basicConfig(level=getattr(logging, environ.get("LOGGING_LEVEL", "INFO")))
app = Flask(__name__)
app.secret_key = environ['FLASK_SECRET']

app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc://{environ['SQL_SERVER_USERNAME']}:{environ['SQL_SERVER_PASSWORD']}@{environ['SQL_SERVER_HOST']}/{environ['SQL_SERVER_DB']}?driver=ODBC+Driver+17+for+SQL+Server"
db = SQLAlchemy(app)
db_Base = automap_base()
with app.app_context():
    # Reflect the database schema
    db_Base.prepare(db.engine)

#logging.debug(f"Found these database attribute:\n{dir(db_Base.classes)}")
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

#############################
### LOGIN ROUTE DECORATOR ###
#############################
def login_required():
    def decorator(function_to_protect):
        @wraps(function_to_protect)
        def wrapper(*args, **kwargs):
            app.logger.debug(f"login_required API call")
            if session.get('name'):
                req_acct = db.session.query(AGENT).get(session['id'])
                if req_acct:
                    req_acct.last_login = datetime.now(timezone.utc)
                    db.session.commit()
                    return function_to_protect(*args, **kwargs)
            else:
                return jsonify({"message":"Try logging in!"}), 401
        return wrapper
    return decorator

##################################
##### IMPORTED SERVER ROUTES #####
##################################
from auth_routes import *

########################
###### STARTUP!!! ######
########################
if __name__ == '__main__':
    @app.route("/api/health", methods=['GET'])
    def healthcheck_endpoint():
        return jsonify({"message":"Still alive!"})
    
    @app.route("/api/authcheck", methods=['GET'])
    @login_required()
    def authcheck_endpoint():
        logging.info(f"Authcheck by: {session['controller_email']}|{session['name']}")
        return jsonify({"message":"Authenticated!", "agent":session['name'], "email":session['controller_email'], "session_start":session['creation_time']})

    logging.info("Starting server!")
    serve(app, host='0.0.0.0', port=9001)