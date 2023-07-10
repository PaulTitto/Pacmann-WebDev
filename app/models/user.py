from app.extensions import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    tasks = db.relationship('Tasks', back_populates='user')
    projects = db.relationship('Projects', back_populates='user')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    def serialize_with_tasks(self, tasks):
        task_list = [task.serialize() for task in tasks]

        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "tasks": task_list
        }