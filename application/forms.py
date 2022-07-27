from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date

class checkDateInFuture():
    def __init__(self, message):
        self.message = message
    
    def __call__(self, form, field):
        if field.data < date.today():
            raise ValidationError(self.message)

class UserForm(FlaskForm):
    forename = StringField('Forename', validators=[DataRequired(), Length(min=1, max=30)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=1, max=30)])
    submit = SubmitField('Enter')

class TaskForm(FlaskForm):
    task_name = StringField('Task Name', validators=[DataRequired(), Length(min=1, max=20)])
    task_desc = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=100)])
    task_status = SelectField('Status', choices=[('todo', 'todo'), ('done', 'done')])
    due_date = DateField('Due Date', validators=[DataRequired(), checkDateInFuture("Please choose a date in the future")])
    assigned_to = SelectField('Assign To', choices=[])
    submit = SubmitField('Enter')