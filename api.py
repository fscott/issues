# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 Franklin Scott
All Rights Reserved.
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models import Issue, User, Status
import issues_app

app = Flask(__name__)
# this order is important: https://flask-marshmallow.readthedocs.io/en/latest/
ma = Marshmallow(app)
db = SQLAlchemy()

api_version = '/v1'
api_route = '/api'

class IssueSchema(ma.ModelSchema):
    class Meta:
        model = Issue

class StatusSchema(ma.ModelSchema):
    class Meta:
        model = Status

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

issue_schema    = IssueSchema()
status_schema   = StatusSchema()
user_schema     = UserSchema()

def create_test_api():
    return issues_app.create_test_app(app)

def create_test_db(app):
    return issues_app.initialize_db(app)    

@app.route(api_route + '/issues/', methods=['GET'])
def issues():
    issues = db.session.query(Issue).all()
    results = {}
    if issues:
        for issue in issues:
            results[issue.id] = issue_schema.dump(issue)
        return jsonify(results)
    else:
        return jsonify("no issues found"), 404
    

@app.route('/api/issue/<id>', methods=['GET'])
def issue_detail(id):
    issue = db.session.query(Issue).get_or_404(id)
    result = issue_schema.dump(issue)
    return jsonify(result)

@app.route('/api/issue/add', methods=['POST'])
def issue_add():
    title = request.args.get('title')
    if title:
        issue = Issue(title=title)
        db.session.add(issue)
        db.session.commit()
        return issue_schema.jsonify(issue)
    else:
        return jsonify("provide a title to add a new issue"), 400

@app.route('/api/issue/assign', methods=['POST'])
def issue_assign():
    user_id = request.args.get('user_id')
    issue_id = request.args.get('issue_id')
    issue = db.session.query(Issue).get(issue_id)
    user = db.session.query(User).get(user_id)
    if user and issue:
        issue.assignee = user
        db.session.commit()
        return issue_schema.jsonify(issue)
    else:
        return jsonify("provide a valid issue id and user id"), 400

@app.route('/api/user/add', methods=['POST'])
def user_add():
    name = request.args.get('name')
    email = request.args.get('email')
    if name and email:
        if not db.session.query(User).filter((User.name == name) | (User.email == email)).first():
            user = User(name=name, email=email)
            db.session.add(user)
            db.session.commit()
            return user_schema.jsonify(user)
        else:
            return jsonify("user name or email already taken"), 400
    else:
        return jsonify("provide a user name and email address"), 400

@app.route('/api/user', methods=['GET'])
def user_detail():
    name = request.args.get('name')
    if name:
        return jsonify(get_user_by_name(name))
    else:
        return "provide a name", 404      

def get_user_by_name(name):
    user = db.session.query(User).filter(name == name).first()
    result = user_schema.dump(user)
    return result

if __name__ == '__main__':
    app = issues_app.create_prod_app(app)
    ma = Marshmallow(app)
    db = issues_app.initialize_db(app)
    app.run()
                     