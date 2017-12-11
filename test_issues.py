# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 Franklin Scott
All Rights Reserved.
"""

import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import api
import tempfile
import issues_app


class APITests(unittest.TestCase):

    #mapp = Flask(__name__)
    db = SQLAlchemy()
    path_to_db = 'data/test.db'

    def setUp(self):
        self.mapp = api.create_test_api()
        self.db = api.create_test_db(self.mapp)
        print(self.mapp.url_map)
        self.client = self.mapp.test_client()

    def tearDown(self):
        os.remove(self.path_to_db)

    def test_add_user(self):
        res = self.client.get('api/user/add', query_string=dict(name='franklin',email='franklinscott@gmail.com'))
        assert res.status_code == 405
        res = self.client.post('api/user/add', query_string=dict(name='franklin',email='franklinscott@gmail.com'))
        assert res.status_code == 200
        assert b'id' in res.data

    def test_get_all_issues(self):
        res = self.client.get('/api/issues/')
        assert res.data

        

