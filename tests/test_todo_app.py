from flask import url_for
from application import app, db
from application.models import *
from flask_testing import TestCase
from datetime import date, timedelta

class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI = 'sqlite:///test-app.db',
            WTF_CSRF_ENABLED = False,
            DEBUG = True,
            SECRET_KEY = 'KSCBV DV VH D'
        )

        return app

    def setUp(self): # runs before each test
        db.create_all()
        user1 = User(forename = 'Sample', surname = 'User')
        task1 = Task(task_name = 'Sample Task', task_desc = 'A sample task for unit tests', task_status = 'todo', due_date = date.today() + timedelta(30), assigned_to = 1)
        db.session.add(user1)
        db.session.add(task1)
        db.session.commit()
    
    def tearDown(self): # runs after every test
        db.session.remove()
        db.drop_all()

class TestHomeView(TestBase):
    def test_get_home(self):
        response = self.client.get(url_for('index'))
        self.assert200(response)
        self.assertIn(b'ToDo App', response.data)
    
    def test_get_users(self):
        response = self.client.get(url_for('view_all_users'))
        self.assert200(response)
        self.assertIn(b'User, Sample', response.data)
    
    def test_get_tasks(self):
        response = self.client.get(url_for('view_all_tasks'))
        self.assert200(response)
        self.assertIn(b'Sample Task', response.data)
        self.assertIn(b'User, Sample', response.data)
    
    def test_get_add_u(self):
        response = self.client.get(url_for('add_user'))
        self.assert200(response)
        self.assertIn(b'Forename', response.data)
    
    def test_get_add_t(self):
        response = self.client.get(url_for('create_new_task'))
        self.assert200(response)
        self.assertIn(b'Task Name', response.data)
    
    def test_get_update_u(self):
        response = self.client.get(url_for('update_user', id=1))
        self.assert200(response)
        self.assertIn(b'Forename', response.data)
    
    def test_get_update_t(self):
        response = self.client.get(url_for('update_task', id=1))
        self.assert200(response)
        self.assertIn(b'Task Name', response.data)
    
    def test_get_delete_u(self):
        response = self.client.get(
            url_for('delete_user', id=1),
            follow_redirects = True
        )
        self.assert200(response)
        self.assertNotIn(b'User, Sample', response.data)

    def test_get_delete_t(self):
        response = self.client.get(
            url_for('delete_task', id=1),
            follow_redirects = True
        )
        self.assert200(response)
        self.assertNotIn(b'Sample Task', response.data)

class TestPostRequests(TestBase):
    def test_post_add_u(self):
        response = self.client.post(
            url_for('add_user'),
            data = dict(forename = 'Alice', surname = 'Jones'),
            follow_redirects = True
        )

        self.assert200(response)
        # self.assertIn(b'Jones, Alice', response.data)
        assert User.query.filter_by(forename='Alice').first() is not None

    def test_post_update_u(self):
        response = self.client.post(
            url_for('update_user', id=1),
            data = dict(forename='New', surname='Data'),
            follow_redirects=True
        )

        self.assert200(response)
        assert User.query.filter_by(forename='New').first() is not None
        assert User.query.filter_by(forename='Sample').first() is None
    
    def test_post_add_t(self):
        response = self.client.post(
            url_for('create_new_task'),
            data = dict(
                task_name = 'Another Sample', 
                task_desc='Yet another sample task', 
                task_status='todo', 
                due_date = date.today() + timedelta(30), 
                assigned_to=1
                ),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertIn(b'Another Sample', response.data)
    
    def test_post_update_t(self):
        response = self.client.post(
            url_for('update_task', id=1),
            data = dict(
                task_name = 'Updated Name', 
                task_desc='New description of task', 
                task_status='todo', 
                due_date = date.today() + timedelta(14), 
                assigned_to=1
                ),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertIn(b'Updated Name', response.data)