# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 Franklin Scott
All Rights Reserved.
"""

import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from api import create_test_api, create_test_db
import tempfile
import issues_app
import json


class APITests(unittest.TestCase):

    db = SQLAlchemy()
    path_to_db = 'data/test.db'
    
    @classmethod
    def setUpClass(cls):
        cls.mapp = create_test_api()
        cls.db = create_test_db(cls.mapp)
        cls.client = cls.mapp.test_client()

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.path_to_db)

    def test_add_user(self):
        res = self.client.get('api/user/add', query_string=dict(name='franklin',email='franklinscott@gmail.com'))
        assert res.status_code == 405
        res = self.client.post('api/user/add', query_string=dict(name='franklin',email='franklinscott@gmail.com'))
        assert res.status_code == 200
        data = json.loads(res.data.decode())
        assert data['name'] == 'franklin'
        assert data['email'] == 'franklinscott@gmail.com'
        id = data['id']
        res = self.client.get('api/user', query_string=dict(name='franklin'))
        data = json.loads(res.data.decode())
        assert data[0]['id'] == id
        assert isinstance(data[0]['id'], int) and data[0]['id'] > -1
    
    def test_add_issue(self):
        res = self.client.post('api/issue/add', query_string=dict(title='do this'))
        assert res.status_code == 200
        data = json.loads(res.data.decode())
        assert data['title'] == 'do this'
        assert isinstance(data['id'], int) and data['id'] > -1

    def test_assign_issue(self):
        res = self.client.post('api/issue/add', query_string=dict(title='do this2'))
        issue_id = json.loads(res.data.decode())['id']
        res = self.client.post('api/user/add', query_string=dict(name='harriet',email='harriet@gmail.com'))
        user_id = json.loads(res.data.decode())['id']
        res = self.client.post('api/issue/assign', query_string=dict(user_id=user_id, issue_id=issue_id))
        assert res.status_code == 200
        data = json.loads(res.data.decode())
        assert data['title'] == 'do this2'
        assert data['assignee'] == user_id
        assert isinstance(data['id'], int) and data['id'] > -1        

    def test_get_all_issues(self):
        res = self.client.get('api/issues/')
        assert res.status_code == 200

        

