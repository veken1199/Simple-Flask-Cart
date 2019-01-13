from flask import Blueprint, jsonify, session
from database.models.user import users_schema, User

user_route = Blueprint('user', __name__, url_prefix='/user')


@user_route.route("")
def get_users():
    users = User.query.all()
    if 'name' in session:
        print(session['name'])
    session['name'] = 'veken'
    return jsonify({'data': users_schema.dump(users).data}), 200

