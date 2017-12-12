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


class APITests(unittest.TestCase):

    #mapp = Flask(__name__)
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
        assert 'id' in res.data.decode()
        assert '"name": "franklin"' in res.data.decode()
    
    def test_add_issue(self):
        res = self.client.post('api/issue/add', query_string=dict(title='dothis'))
        #print(res.status_code)
        assert res.status_code == 200
        assert 'id' in res.data.decode()
        assert '"title": "dothis"' in res.data.decode()

    def test_get_all_issues(self):
        res = self.client.get('api/issues/')
        assert res.status_code == 200

        

