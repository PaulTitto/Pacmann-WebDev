from flask import request, jsonify
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.task import taskBp
from app.models.task import Tasks


# Get All Task
@taskBp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required(locations=['headers'])
def get_all_task():
    limit = request.args.get('limit', 10)
    current_user_id = get_jwt_identity()

    if type(limit) is not int:
        return jsonify({
            "message": "Invalid parameter"
        }), 400

    tasks = Tasks.query.filter_by(user_id=current_user_id).all()

    result = []
    for task in tasks:
        result.append(task.serialize())

    return jsonify({
        "success": True,
        "data": result
    }), 200


# Get Task By ID
@taskBp.route('/<int:id>', methods=['GET'], strict_slashes=False)
@jwt_required(locations=['headers'])
def get_task_by_id(id):
    current_user_id = get_jwt_identity()

    task = Tasks.query.filter_by(id=id).first()

    if not task:
        return jsonify({"message": "Task not found!"}), 404

    if current_user_id != task.user_id:
        return jsonify({
            "message": "Unauthorized Action"
        }), 422

    return jsonify({
        "success": True,
        "data": task.serialize(),
    }), 200


# Create Task
@taskBp.route('/', methods=['POST'], strict_slashes=False)
@jwt_required(locations=['headers'])
def create_task():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    title = data['title']
    description = data.get('description', None)
    project_id = data.get('project_id', None)

    if not title or not current_user_id:
        return jsonify({
            "message": "Incomplete data"
        }), 422

    new_task = Tasks(title=title, description=description, user_id=current_user_id, project_id=project_id)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "success": True,
        "data": new_task.serialize()
    }), 200


# Edit Task
@taskBp.route('/<int:id>', methods=['PUT'], strict_slashes=False)
@jwt_required(locations=['headers'])
def edit_task(id):
    data = request.get_json()
    current_user_id = get_jwt_identity()

    new_title = data['title']
    new_description = data.get('description', None)

    task = Tasks.query.filter_by(id=id).first()

    if not task:
        return jsonify({"message": "Task not found!"}), 404

    if not new_title:
        return jsonify({"message": "Title is required!"}), 400

    if current_user_id != task.user_id:
        return jsonify({
            "message": "Unauthorized Action"
        }), 422

    task.title = new_title
    task.description = new_description

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Task sucessfully updated!"
    }), 200


# Delete Task
@taskBp.route('<int:id>', methods=['DELETE'], strict_slashes=False)
@jwt_required(locations=['headers'])
def delete_task(id):
    task = Tasks.query.filter_by(id=id).first()
    current_user_id = get_jwt_identity()

    if not task:
        return jsonify({"message": "Task not found!"}), 404

    if current_user_id != task.user_id:
        return jsonify({
            "message": "Unauthorized Action"
        }), 422

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Task has been deleted sucessfully!"
    }), 200


# Update Tasks's Status
@taskBp.route("/status/<int:id>", methods=["PUT"], strict_slashes=False)
@jwt_required(locations=["headers"])
def update_status(id):
    current_user_id = get_jwt_identity()

    task = Tasks.query.filter_by(id=id).first()

    if not task:
        return jsonify({"message": "Task not found!"}), 404

    if current_user_id != task.user_id:
        return jsonify({
            "message": "Unauthorized Action"
        }), 422

    data = request.get_json()
    status = data.get("status")

    task.status = status
    db.session.commit()

    return jsonify({
        "success": True, "message": "Status updated successfully"
    }), 200