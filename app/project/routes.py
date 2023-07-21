from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db

from app.project import projectBp
from app.models.task import Tasks
from app.models.user import Users
from app.models.project import Projects


# Get All Project
@projectBp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required(locations=['headers'])
def get_all_project():
    limit = request.args.get('limit', 10)
    current_user_id = get_jwt_identity()

    if type(limit) is not int:
        return jsonify({
            "message": "Invalid parameter"
        }), 400

    projects = Projects.query.filter_by(user_id=current_user_id).all()

    result = []
    for project in projects:
        result.append(project.serialize())

    return jsonify({
        "success": True,
        "data": result
    }), 200


# Create Project
@projectBp.route('/', methods=['POST'], strict_slashes=False)
@jwt_required(locations=['headers'])
def create_project():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    title = data['title']

    if not title or not current_user_id:
        return jsonify({
            "message": "Incomplete data"
        }), 422

    new_project = Projects(title=title, user_id=current_user_id)

    db.session.add(new_project)
    db.session.commit()

    return jsonify({
        "success": True,
        "data": new_project.serialize()
    }), 200


# Get Project with Tasks
@projectBp.route('/<int:id>/tasks', methods=['GET'], strict_slashes=False)
@jwt_required(locations=['headers'])
def get_project_with_tasks(id):
    current_user_id = get_jwt_identity()

    project = Projects.query.filter_by(id=id).first()

    if current_user_id != project.user_id:
        return jsonify({
            "message": "Unauthorized Action"
        }), 422

    tasks = Tasks.query.filter_by(project_id=id).all()

    return jsonify({
        "data": project.serialize_with_tasks(tasks)
    })
