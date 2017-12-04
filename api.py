from flask import Flask, jsonify, request
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
#from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/test.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

api_version = '/v1'
api_route = '/api'

#Base = declarative_base()

class Issue(db.Model):
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
        return "<Issue(title={0.title}, description={0.description})>".format(self)


class Status(db.Model):
    """docstring for Status"""
    __tablename__   = 'statuses'

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String)

    issues          = db.relationship("Issue")

    def __repr__(self):
        return "<Status(name={0}.name)>".format(self=self)

class User(db.Model):
    """docstring for User"""
    __tablename__   = 'users'

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String)
    email           = db.Column(db.String)

    issues          = db.relationship("Issue")

    def __repr__(self):
        return "<User(name={0}.name, email={0}.email)>".format(self=self)


class IssueSchema(ma.ModelSchema):
    class Meta:
        model = Issue

class StatusSchema(ma.ModelSchema):
    class Meta:
        model = Status

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

db.create_all()

issue_schema    = IssueSchema()
status_schema   = StatusSchema()
user_schema     = UserSchema()

@app.route('/api/issues/')
def issues():
    issues = db.session.query(Issue).all()
    results = {}
    for issue in issues:
        results[issue.id] = issue_schema.dump(issue)
    return jsonify(results)

@app.route('/api/issue/<id>')
def issue_detail(id):
    issue = Issue(id=id)
    result = issue_schema.dump(issue)
    return jsonify(result)

@app.route('/api/issue/add')
def issue_add():
    title = request.args.get('title')
    if title:
        issue = Issue(title=title)
        db.session.add(issue)
        db.session.commit()
        return issue_schema.jsonify(issue)
    else:
        return "provide a title to add a new issue", 400


if __name__ == '__main__':

    app.run(debug=True)

                      
#if __name__ == '__main__':
#    app.run(host='pi2.int.franklinscott.com', port=8070)                      