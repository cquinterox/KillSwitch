"""
Routes and views for the flask application.
"""

import json
from datetime import datetime
from flask import render_template, request
from KillSwitch_Flask import app
from KillSwitch_Flask import frontier

with open('conf.json') as jsonData:
    conf = json.load(jsonData)

@app.route('/', methods=["GET","POST"])
def index(): 
    with frontier.RouterApi(conf["routerAddress"], conf["routerPassword"]) as api:
        status = api.getAccessControlRuleStatus(conf["ruleId"])

    if request.method == 'POST':
        newStatus = True if request.form["ruleOption"]  == "True" else False
        if status != newStatus:
            with frontier.RouterApi(conf["routerAddress"], conf["routerPassword"]) as api:
                success = api.toggleAccessControlRule(conf["ruleId"], newStatus)
                if success:
                    status = newStatus

    return render_template(
        'index.html',
        title='Internet KillSwitch',
        ruleStatus=status,
        year=datetime.now().year,
    )