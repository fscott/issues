from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#from issues import * 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/test.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

api = Api(app)
api_version = '/v1'
api_route = '/api'

Base = declarative_base()

class Issue(Base):
    """docstring for Issue"""
    __tablename__   = 'issues'

    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String, nullable=False)
    description     = db.Column(db.String)
    assignee_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
    status_id       = db.Column(db.Integer, db.ForeignKey('statuses.id'))

    status          = db.relationship("Status", back_populates="issues")
    assignee        = db.relationship("User", back_populates="issues")

    def __repr__(self):
        return "<Issue(title={0}.title, description={0}.description)>".format(self)


class Status(Base):
    """docstring for Status"""
    __tablename__   = 'statuses'

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String)

    issues          = db.relationship("Issue")

    def __repr__(self):
        return "<Status(name={0}.name)>".format(self)

class User(Base):
    """docstring for User"""
    __tablename__   = 'users'

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String)
    email           = db.Column(db.String)

    issues          = db.relationship("Issue")

    def __repr__(self):
        return "<User(name={0}.name, email={0}.email)>".format(self)


class IssueSchema(Schema):
    class Meta:
        model = Issue

class StatusSchema(Schema):
    class Meta:
        model = Status

class UserSchema(Schema):
    class Meta:
        model = User

db.create_all()

issue_schema    = IssueSchema()
status_schema   = StatusSchema()
user_schema     = UserSchema()

# Issue
# shows a single issue and lets you delete an issue
class IssueId(Resource):
    def get(self, issue_id):
        issue = Issue(id=issue_id)
        return issue_schema.dump(issue).data, 200

    def delete(self, issue_id):
        return '', 501

class IssueAdd(Resource):
    def put(self, title):
        issue = Issue(title=title)
        db.session.add(issue)
        db.session.commit()
        return issue_schema.dump(issue).data, 200


# IssueList
# shows a list of all issues, and lets you POST to add new issues
class IssueListAPI(Resource):
    def get(self):
        issues = Issue.all()
        return issue_schema.dump(issues, many=True), 200

    def post(self):
        return '', 501

##
## Actually setup the Api resource routing here
##
api.add_resource(IssueListAPI, api_route + '/issues', api_route + api_version + '/issues')
api.add_resource(IssueId, api_route + '/issue/<issue_id>', api_route + api_version + '/issue/<issue_id>')
api.add_resource(IssueAdd, api_route + '/issue/add/<title>', api_route + api_version + '/issue/add/<title>')


if __name__ == '__main__':

    app.run(debug=True)

                      
#if __name__ == '__main__':
#    app.run(host='pi2.int.franklinscott.com', port=8070)                      