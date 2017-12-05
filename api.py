from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# this order is important: https://flask-marshmallow.readthedocs.io/en/latest/
ma = Marshmallow(app)

api_version = '/v1'
api_route = '/api'

# https://stackoverflow.com/a/19849375
from models import db, Issue, User, Status
db.app = app
db.init_app(app)
db.create_all()

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


@app.route(api_route + '/issues/', methods=['GET'])
def issues():
    issues = db.session.query(Issue).all()
    results = {}
    if issues:
        for issue in issues:
            results[issue.id] = issue_schema.dump(issue)
    else:
        return jsonify("no issues found"), 404
    return jsonify(results)

@app.route('/api/issue/<id>')
def issue_detail(id):
    issue = db.session.query(Issue).get_or_404(id)
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
        return jsonify("provide a title to add a new issue"), 400

@app.route('/api/issue/assign')
def issue_assign():
    user = request.args.get('user')
    issue_id = request.args.get('issue_id')
    issue = db.session.query(Issue).get(issue_id)
    if user:
        if issue:
            db.session.update(Issue).where(id == issue_id).values(assignee = user.id)
            db.session.commit()
            return issue_schema.jsonify(issue)
        else:
            return jsonify("provide a valid issue id"), 400
    else:
        return jsonify("provide a valid user name"), 400

@app.route('/api/user/add')
def user_add():
    user = request.args.get('user')
    email = request.args.get('email')
    if user and email:
        if db.session.query(User).filter(name == user | email == email).first():
            user = User(name=user, email=email)
            db.session.add(user)
            db.session.commit()
            return issue_schema.jsonify(user)
        else:
            return jsonify("user name or email already taken"), 400
    else:
        return jsonify("provide a user name and email address"), 400

if __name__ == '__main__':
    app.run(debug=True)

                      
#if __name__ == '__main__':
#    app.run(host='pi2.int.franklinscott.com', port=8070)                      