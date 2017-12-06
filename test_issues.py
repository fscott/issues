import sqlite3
import unittest
from models import Issue, User, Status
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine
from sqlalchemy.schema import MetaData
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from api import app, db

class APITests(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/test.db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        #app.run()

    def test_get_all_issues(self):
        res = self.app.get('/api/issues/')
        assert res.data

        

