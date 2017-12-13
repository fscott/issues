# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 Franklin Scott
All Rights Reserved.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Issue(db.Model):
    """docstring for Issue"""
    __tablename__   = 'issues'

    id              = Column(Integer, primary_key=True)
    title           = Column(String, nullable=False)
    description     = Column(String)
    assignee_id     = Column(Integer, ForeignKey('users.id'))
    status_id       = Column(Integer, ForeignKey('statuses.id'))

    status          = relationship("Status", back_populates="issues")
    assignee        = relationship("User", back_populates="issues")

    def __repr__(self):
        return "<Issue(title={0.title},\
                 description={0.description})>".format(self)


class Status(db.Model):
    """docstring for Status"""
    __tablename__   = 'statuses'

    id              = Column(Integer, primary_key=True)
    name            = Column(String, unique=True)

    issues          = relationship("Issue")

    def __repr__(self):
        return "<Status(name={0.name})>".format(self)


class User(db.Model):
    """docstring for User"""
    __tablename__   = 'users'

    id              = Column(Integer, primary_key=True)
    name            = Column(String, nullable=False)
    email           = Column(String, unique=True, nullable=False)

    issues          = relationship("Issue")

    def __repr__(self):
        return "<User(name={0.name}, email={0.email})>".format(self)
