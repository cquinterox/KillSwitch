"""
Routes and views for the flask application.
"""

import json
from datetime import datetime
from flask import render_template, request, jsonify
from KillSwitch_Flask import app
from KillSwitch_Flask import frontier

with open("conf.json") as jsonData:
    conf = json.load(jsonData)

@app.route("/", methods=["GET","POST"])
def index(): 
    rules=conf["accessControlRules"]
    with frontier.RouterApi(conf["routerAddress"], conf["routerPassword"]) as api:
        for rule in rules:
            rule["active"] = api.getAccessControlRuleStatus(rule["ruleId"])

    return render_template(
        "index.html",
        title="Internet KillSwitch",
        year=datetime.now().year,
        accessControlRules=rules
    )

@app.route("/ruleStatus", methods=["GET"])
def getRuleStatus():
    ruleId = request.args.get("ruleId", default=-1, type=int)
    with frontier.RouterApi(conf["routerAddress"], conf["routerPassword"]) as api:
        status = api.getAccessControlRuleStatus(ruleId)
            
    return jsonify({"ruleId": ruleId, "active": status})

@app.route("/ruleStatus", methods=["POST"])
def setRuleStatus():
    ruleId = request.form.get("ruleId", default=-1, type=int)
    newStatus = request.form.get("active", default=False, type=bool)  
    with frontier.RouterApi(conf["routerAddress"], conf["routerPassword"]) as api:
        success = api.toggleAccessControlRule(ruleId, newStatus)

    return jsonify({"success": success})

