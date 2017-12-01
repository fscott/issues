from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from sqlalchemy.orm import sessionmaker
from issues import * 


app = Flask(__name__)
api = Api(app)
api_version = '/v1'
api_route = '/api'

ISSUES = {}


def abort_if_issue_doesnt_exist(issue_id):
    if issue_id not in ISSUES:
        abort(404, message="Issue {} doesn't exist".format(issue_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Issue
# shows a single issue and lets you delete an issue
class IssueAPI(Resource):
    def get(self, issue_id):
        abort_if_issue_doesnt_exist(issue_id)
        return ISSUES[issue_id]

    def delete(self, issue_id):
        abort_if_issue_doesnt_exist(issue_id)
        del ISSUES[issue_id]
        return '', 204

    def put(self, issue_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        ISSUES[issue_id] = task
        return task, 201


# IssueList
# shows a list of all issues, and lets you POST to add new issues
class IssueListAPI(Resource):
    def get(self):
        return ISSUES

    def post(self):
        args = parser.parse_args()
        issue_id = int(max(ISSUES.keys()).lstrip('issue')) + 1
        issue_id = 'issue%i' % issue_id
        ISSUES[issue_id] = {'task': args['task']}
        return ISSUES[issue_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(IssueListAPI, api_route + '/issues', api_route + api_version + '/issues')
api.add_resource(IssueAPI, api_route + '/issues/<issue_id>', api_route + api_version + '/issues/<issue_id>')


if __name__ == '__main__':
    db = IssuesDB('sqlite:///data/test.db')
    Session = sessionmaker()
    Session.configure(bind=db.engine)
    fuser = User(name='franklin', email='franklinscott@gmail.com')
    sess = Session()
    sess.add(fuser)
    sess.commit()
    sess.close()
    app.run(debug=True)

                      
#if __name__ == '__main__':
#    app.run(host='pi2.int.franklinscott.com', port=8070)                      