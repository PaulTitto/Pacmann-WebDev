from app.extensions import db


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', back_populates='projects')
    tasks = db.relationship('Tasks', back_populates='projects')

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id
        }

    def serialize_with_tasks(self, tasks):
        task_list = [task.serialize() for task in tasks]

        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "tasks": task_list
        }