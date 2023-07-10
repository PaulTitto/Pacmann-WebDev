from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db

from app.user import userBp
from app.models.task import Tasks
from app.models.user import Users


# Get All Users
@userBp.route('/', methods=['GET'], strict_slashes=False)
def get_all_users():
    limit = request.args.get('limit', 10)

    if type(limit) is not int:
        return jsonify({
            "message": "Invalid parameter"
        }), 400

    users = db.session.execute(db.select(Users).limit(limit)).scalars()

    result = []
    for user in users:
        result.append(user.serialize())

    return jsonify({
        "success": True,
        "data": result
    }), 200


# Get User By ID
@userBp.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(id):
    user = Users.query.filter_by(id=id).first()

    if not user:
        return jsonify({
            "message": "User doesn't exists!"
        })

    return jsonify({
        "success": True,
        "data": user.serialize()
    })


# Get User with Task
@userBp.route('/tasks', methods=['GET'], strict_slashes=False)
@jwt_required(locations=['headers'])
def get_user_with_task():
    current_user_id = get_jwt_identity()
    user = Users.query.filter_by(id=current_user_id).first()
    tasks = Tasks.query.filter_by(user_id=current_user_id).all()

    return jsonify({
        "user": user.serialize_with_tasks(tasks)
    })