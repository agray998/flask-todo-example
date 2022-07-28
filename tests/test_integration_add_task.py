from flask_testing import LiveServerTestCase
from selenium import webdriver
from urllib.request import urlopen
from flask import url_for
from application import app, db
from application.models import *
from application.forms import *
from datetime import date, timedelta

class TestBase(LiveServerTestCase):
    TEST_PORT = 5050

    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI = 'sqlite:///test-app.db',
            LIVESERVER_PORT = self.TEST_PORT,
            DEBUG = True,
            TESTING = True
        )

        return app
    
    def setUp(self):
        db.create_all()
        sample_user = User(forename="John", surname="Smith")
        db.session.add(sample_user)
        db.session.commit()
        options = webdriver.chrome.options.Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(f'http://localhost:{self.TEST_PORT}/add-task')

    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()
    
    def test_server_connectivity(self):
        response = urlopen(f'http://localhost:{self.TEST_PORT}/add-task')
        assert response.status == 200

class TestAddUser(TestBase):
    def submit_input(self, test_case, test_valid = False):
        task_name_field = self.driver.find_element_by_xpath('/html/body/div/form/input[2]')
        task_desc_field = self.driver.find_element_by_xpath('/html/body/div/form/textarea')
        date_field = self.driver.find_element_by_xpath('/html/body/div/form/input[3]')
        status_field = self.driver.find_element_by_xpath('/html/body/div/form/select[1]')
        assigned_to_field = self.driver.find_element_by_xpath('/html/body/div/form/select[2]')
        submit = self.driver.find_element_by_xpath('/html/body/div/form/input[4]')
        task_name_field.send_keys(test_case[0])
        task_desc_field.send_keys(test_case[1])
        if test_valid:
            date_field.clear()
        status_field.send_keys(test_case[2])
        assigned_to_field.send_keys(test_case[3])
        submit.click()
    
    def test_add_task(self):
        test_case = "Sample Task", "A task for the integration test", 'todo', 'John Smith'
        self.submit_input(test_case)
        assert list(Task.query.all()) != []
        assert Task.query.filter_by(task_name="Sample Task").first() is not None

    def test_add_task_validation(self):
        test_case = "Sample Task", "A task for the integration test", 'todo', 'John Smith'
        self.submit_input(test_case, test_valid=True)
        assert list(Task.query.all()) == []
        assert Task.query.filter_by(task_name="Sample Task").first() is None
        assert self.driver.find_element_by_xpath('/html/body/div[2]/p[2]').text == 'Please choose a date in the future'