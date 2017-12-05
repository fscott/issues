from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
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
        return "<Issue(title={0.title}, description={0.description})>".format(self)


class Status(db.Model):
    """docstring for Status"""
    __tablename__   = 'statuses'

    id              = Column(Integer, primary_key=True)
    name            = Column(String)

    issues          = relationship("Issue")

    def __repr__(self):
        return "<Status(name={0.name})>".format(self)

class User(db.Model):
    """docstring for User"""
    __tablename__   = 'users'

    id              = Column(Integer, primary_key=True)
    name            = Column(String)
    email           = Column(String)

    issues          = relationship("Issue")

    def __repr__(self):
        return "<User(name={0.name}, email={0.email})>".format(self)




