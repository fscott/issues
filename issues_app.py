# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 Franklin Scott
All Rights Reserved.
"""

from models import db


def create_test_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    db.init_app(app)
    app.app_context().push()
    return app


def create_prod_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/prod.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()
    return app


def initialize_db(app):
    db.app = app
    db.init_app(app)
    db.create_all()
    return db
