# STL
import logging
from os import environ

# EXT

from flask import Flask, jsonify

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from waitress import serve


from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base


from flask import Flask, session
############################
#### APP AND DB OBJECTS ####
############################
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.secret_key = environ['FLASK_SECRET']
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc://{environ['SQL_SERVER_USERNAME']}:{environ['SQL_SERVER_PASSWORD']}@{environ['SQL_SERVER_HOST']}/{environ['SQL_SERVER_DB']}?driver=ODBC+Driver+17+for+SQL+Server"
db = SQLAlchemy(app)
db_Base = automap_base()
with app.app_context():
    # Reflect the database schema
    db_Base.prepare(db.engine)

AGENT = db_Base.classes.agent
BUILDING = db_Base.classes.building
BUILDING_RESOURCE_NET_MAINTENANCE_COST = db_Base.classes.building_resource_net_maintenance_cost
BUILDING_TYPE = db_Base.classes.building_type
RESOURCE = db_Base.classes.resource
SHIP = db_Base.classes.ship
SHIP_CARGO = db_Base.classes.ship_cargo
SHIP_RESOURCE_NET_MAINTENANCE_COST = db_Base.classes.ship_resource_net_maintenance_cost
SHIP_TYPE = db_Base.classes.ship_type
SYSTEM = db_Base.classes.system
SYSTEM_RESOURCE_STOCKPILE = db_Base.classes.system_resource_stockpile

#############################
### LOGIN ROUTE DECORATOR ###
#############################
def login_required():
    def decorator(function_to_protect):
        @wraps(function_to_protect)
        def wrapper(*args, **kwargs):
            app.logger.debug(f"login_required API call")
            if session.get('name'):
                req_acct = db.session.query(AGENT).get(session['name'])
                if req_acct:
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
        app.logger.info(f"Authcheck by: {session['email']}|{session['name']}")
        return jsonify({"message":"Authenticated!", "agent":{session['name']}, "email":session['email'], "session_start":session['creation_time']})

    db.init_app(app)
    app.logger.info("Starting server!")
    serve(app, host='0.0.0.0', port=9001)