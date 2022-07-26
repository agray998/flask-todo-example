from application import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key = True)
    task_name = db.Column(db.String(20))
    task_desc = db.Column(db.String(100))
    task_status = db.Column(db.String(4))
    due_date = db.Column(db.Date)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.uid'))
    def __str__(self):
        return f"{self.task_status.upper()} {self.task_name}: {self.task_desc}. Due {self.due_date}."

class User(db.Model):
    uid = db.Column(db.Integer, primary_key = True)
    forename = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    tasks = db.relationship('Task', backref='user')
    def __str__(self):
        return f"{self.surname}, {self.forename}"
