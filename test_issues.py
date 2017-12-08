# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 Franklin Scott
All Rights Reserved.
"""

import unittest
import os
from api import app, db

class APITests(unittest.TestCase):

    def setUp(self):
        self.path_to_db = 'data/test.db'
        self.db_info = 'sqlite:///' + self.path_to_db
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_info
        app.config['TESTING'] = True
        self.app = app.test_client()
        from models import db, Issue, User, Status
        db.app = self.app
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        os.remove(self.path_to_db)

    def test_add_user(self):
        res = self.app.get('api/user/add', query_string=dict(name='franklin',email='franklinscott@gmail.com'))
        assert res.status_code == 405
        res = self.app.get('api/user/add', query_string=dict(name='franklin',email='franklinscott@gmail.com'))
        assert res.status_code == 200

    def test_get_all_issues(self):
        res = self.app.get('/api/issues/')
        assert res.data

        

