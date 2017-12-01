from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Issue(Base):
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
        return "<Issue(title={0}.title, description={0}.description)>".format(self)


class Status(Base):
    """docstring for Status"""
    __tablename__   = 'statuses'

    id              = Column(Integer, primary_key=True)
    name            = Column(String)

    issues          = relationship("Issue")

    def __repr__(self):
        return "<Status(name={0}.name)>".format(self)

class User(Base):
    """docstring for User"""
    __tablename__   = 'users'

    id              = Column(Integer, primary_key=True)
    name            = Column(String)
    email           = Column(String)

    issues          = relationship("Issue")

    def __repr__(self):
        return "<User(name={0}.name, email={0}.email)>".format(self)

class IssuesDB(object):
    """docstring for IssuesDB"""
    username = ""
    password = ""
    db_type  = ""
    engine   = None

    def __init__(self, db_type="sqlite:///:memory:"):
        self.db_type = db_type
        self.engine = create_engine(self.db_type, echo=False) # echo True to debug
        Base.metadata.create_all(self.engine)
        







