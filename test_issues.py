import sqlite3
import unittest
from issues import Issue, User, Status, IssuesDB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine
from sqlalchemy.schema import MetaData 


class DbTests(unittest.TestCase):
    db      = None

    def setUp(self):
        self.db = IssuesDB()

    def getSession(self):
        return self.db.Session()

    def test_connect_db(self):
        self.assertIsInstance(self.db.engine, Engine)

    def test_create_user(self):
        fuser = User(name='franklin', email='franklinscott@gmail.com')
        self.assertEqual(fuser.name,'franklin')
        self.assertEqual(fuser.email, 'franklinscott@gmail.com')

    def test_add_user(self):
        fuser = User(name='franklin', email='franklinscott@gmail.com')
        sess = self.getSession()
        sess.add(fuser)
        new_fuser = sess.query(User).filter_by(name='franklin').first()
        self.assertEqual(fuser,new_fuser)
        sess.commit()
        sess.close()
        new_sess = self.getSession()
        new_new_fuser = sess.query(User).filter_by(name='franklin').first()
        self.assertEqual(new_new_fuser.email,'franklinscott@gmail.com')
        new_sess.commit()
        new_sess.close()

    def test_create_issue(self):
        fissue = Issue(title='franklin do this', description='blah')
        self.assertEqual(fissue.title,'franklin do this')
        self.assertEqual(fissue.description, 'blah')

    def test_add_issue(self):
        fissue = Issue(title='franklin do this', description='blah')
        sess = self.getSession()
        sess.add(fissue)
        new_fissue = sess.query(Issue).filter_by(title='franklin do this').first()
        self.assertEqual(fissue,new_fissue)
        sess.commit()
        sess.close()
        new_sess = self.getSession()
        new_new_fissue = sess.query(Issue).filter_by(title='franklin do this').first()
        self.assertEqual(new_new_fissue.description,'blah')
        new_sess.commit()
        new_sess.close()

    def test_create_status(self):
        fstatus = Status(name='donedone')
        self.assertEqual(fstatus.name,'donedone')

    def test_add_issue(self):
        fstatus = Status(name='donedone')
        sess = self.getSession()
        sess.add(fstatus)
        new_fstatus = sess.query(Status).filter_by(name='donedone').first()
        self.assertEqual(fstatus,new_fstatus)
        sess.commit()
        sess.close()
        new_sess = self.getSession()
        new_new_fstatus = sess.query(Status).filter_by(name='donedone').first()
        self.assertEqual(new_new_fstatus.name,'donedone')
        new_sess.commit()
        new_sess.close()              

        

