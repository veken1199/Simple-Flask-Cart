from flask import Blueprint, jsonify, session
from database.models.user import users_schema, User
from database.seed import *
from util.response_builder import ApiResponse


user_route = Blueprint('user', __name__, url_prefix='/user')

@user_route.route("")
def reset_data():
    try:
        start_seed(db)
    except:
        return ApiResponse(message="Something wrong happened!", has_error=True).respond()
    return ApiResponse().respond()

