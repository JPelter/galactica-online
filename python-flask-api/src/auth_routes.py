# STL
from datetime import datetime, timedelta, timezone
from functools import wraps
import logging
from email.message import EmailMessage
from os import environ
import secrets
import smtplib
import string

# AUTH
from flask import jsonify, request, session
from server import app, db, AGENT

login_token_minutes = 15 # TIME FOR TOKEN TO EXPIRE AND TOKEN REQUEST RATE LIMIT TIME

@app.route("/api/login-token", methods=['GET'])
def token_request_endpoint():
    # QUERY FOR AGENT OBJECT ON NAME AND EMAIL, CREATE NEW TOKEN!
    logging.info(f"Login token email request for: {request.get_json()['name']}")
    req_acct = db.session.query(AGENT).filter(AGENT.name == request.get_json()['name']).filter(AGENT.controller_email == request.get_json()['controller_email']).first()
    new_token = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    req_acct.login_token = new_token
    logging.info(f"Token generated for: {request.get_json()['controller_email']}|{request.get_json()['name']}")
    db.session.commit()

    # NOW WE SEND USER THE EMAIL CONTAINING THEIR LOGIN TOKEN!
    msg = EmailMessage()
    msg.set_content(f"Hello,\n\nHere is your login token:\n\n\t\t{new_token}\n\nThanks,\nGalactica Team")
    msg['Subject'] = "Galactica Login Token!"
    msg['From'] = environ["SENDER_EMAIL"]
    msg['To'] = request.get_json()["controller_email"]
    s = smtplib.SMTP(environ['SMTP_RELAY'], 587, timeout=15) # try ports 25, 465, 587
    s.starttls()
    s.login(environ["EMAIL_AGENT"], environ["EMAIL_PASSWORD"])
    s.send_message(msg)
    s.quit()
    app.logger.info(f"Token emailed for: {request.get_json()['controller_email']}")
    return jsonify({"message":"Login token sent to email!", "email":request.get_json()["controller_email"]})

@app.route("/api/login-token", methods=['POST'])
def token_post_endpoint():
    app.logger.info(f"Token exchange request for: {request.get_json()['controller_email']} with token: {request.get_json()['login_token']}")
    req_acct = db.session.query(AGENT).filter(AGENT.name == request.get_json()['name']).filter(AGENT.controller_email == request.get_json()['controller_email']).first()
    if req_acct.login_token == request.get_json()["login_token"]:
        session['controller_email'] = request.get_json()["controller_email"]
        session['creation_time'] = datetime.now(timezone.utc)
        session['name'] = req_acct.name
        req_acct.last_login = session['creation_time']
        logging.info(f"Created session cookie for: {request.get_json()['controller_email']}")
        db.session.commit()
        return jsonify({"message":"Token exchanged for authenticating session cookie!", "email":request.get_json()["controller_email"]})
    else:
        logging.info(f"No session cookie for: {request.get_json()['controller_email']}")
        return jsonify({"message":"Expired or incorrect token!", "email":request.get_json()["controller_email"]}), 403
    
@app.route("/api/logout", methods=['GET'])
def logout_endpoint():
    session.clear()
    return jsonify({"message":"Session cookie cleared!"})
