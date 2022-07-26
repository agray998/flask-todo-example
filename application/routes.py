from application import app, db
from application.models import *
from datetime import date, timedelta
from flask import request, redirect, url_for, render_template

@app.route('/')
def index():
    return "ToDo App"

@app.route('/view_tasks')
def view_all_tasks():
    tasks = Task.query.all()
    return render_template('view_all.html', entity='Task', tasks=tasks)

@app.route('/add-task')
def create_new_task():
    name = request.args.get('t_name')
    desc = request.args.get('t_desc')
    user = request.args.get('uid')
    due = request.args.get('due_date', '')
    due_date = date(*(map(int, due.split('-')))) if due else date.today() + timedelta(30)
    task = Task(task_name=name, task_desc=desc, due_date=due_date, task_status='todo', assigned_to=user)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('view_all_tasks'))

@app.route('/update-task/<int:id>/<attribute>/<new_val>')
def update_task(id, attribute, new_val):
    task_to_update = Task.query.get(id)
    if attribute == 'due_date':
        new_val = date(*(map(int, new_val.split('-'))))
    elif attribute == 'assigned_to':
        new_val = int(new_val)
    setattr(task_to_update, attribute, new_val)
    db.session.commit()
    return redirect(url_for('view_all_tasks'))

@app.route('/delete-task/<int:id>')
def delete_task(id):
    task_to_delete = Task.query.get(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('view_all_tasks'))

@app.route('/view-users')
def view_all_users():
    users = User.query.all()
    return render_template('view_all.html', entity='User', tasks=users)

@app.route('/add-user/<forename>/<surname>')
def add_user(forename, surname):
    user = User(forename=forename, surname=surname)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('view_all_users'))

@app.route('/update-user/<int:id>/<attribute>/<new_val>')
def update_user(id, attribute, new_val):
    user_to_update = User.query.get(id)
    setattr(user_to_update, attribute, new_val)
    db.session.commit()
    return redirect(url_for('view_all_users'))

@app.route('/delete-user/<int:id>')
def delete_user(id):
    user_to_delete = User.query.get(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('view_all_users'))