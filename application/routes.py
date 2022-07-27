from application import app, db
from application.models import *
from datetime import date, timedelta
from flask import request, redirect, url_for, render_template
from application.forms import *

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/view-tasks')
def view_all_tasks():
    tasks = Task.query.all()
    return render_template('view_all.html', entity='Task', tasks=tasks)

@app.route('/add-task', methods=['GET', 'POST'])
def create_new_task():
    form = TaskForm()
    users = User.query.all()
    form.assigned_to.choices = [(user.uid, f"{user.forename} {user.surname}") for user in users]
    if form.validate_on_submit():
        t_name = form.task_name.data
        t_desc = form.task_desc.data
        due_date = form.due_date.data
        uid = form.assigned_to.data
        status = form.task_status.data
        new_task = Task(task_name=t_name, task_desc=t_desc, task_status=status, due_date=due_date, assigned_to=uid)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('view_all_tasks'))
    errors = form.due_date.errors
    errors += form.task_name.errors
    return render_template('task_form.html', form = form, errors = errors)

@app.route('/update-task/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task_to_update = Task.query.get(id)
    form = TaskForm()
    users = User.query.all()
    form.assigned_to.choices = [(user.uid, f"{user.forename} {user.surname}") for user in users]
    if form.validate_on_submit():
        task_to_update.task_name = form.task_name.data
        task_to_update.task_desc = form.task_desc.data
        task_to_update.due_date = form.due_date.data
        task_to_update.status = form.task_status.data
        task_to_update.assigned_to = form.assigned_to.data
        db.session.commit()
        return redirect(url_for('view_all_tasks'))
    form.task_name.data = task_to_update.task_name
    form.task_desc.data = task_to_update.task_desc
    form.due_date.data = task_to_update.due_date
    return render_template('task_form.html', form=form)

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

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        forename = form.forename.data
        surname = form.surname.data
        new_user = User(forename=forename, surname=surname)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('view_all_users'))
    return render_template('user_form.html', form=form)

@app.route('/update-user/<int:id>', methods = ['GET', 'POST'])
def update_user(id):
    user_to_update = User.query.get(id)
    form = UserForm()
    if form.validate_on_submit():
        forename, surname = form.forename.data, form.surname.data
        user_to_update.forename = forename
        user_to_update.surname = surname
        db.session.commit()
        return redirect(url_for('view_all_users'))
    form.forename.data = user_to_update.forename
    form.surname.data = user_to_update.surname
    return render_template('user_form.html', form=form)

@app.route('/delete-user/<int:id>')
def delete_user(id):
    user_to_delete = User.query.get(id)
    for task in user_to_delete.tasks:
        db.session.delete(task)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('view_all_users'))