from flask import Blueprint, jsonify, session
from flask_apispec.annotations import doc, marshal_with

from database.seed import db, start_seed
from database.schemas.purchase import PurchaseResponseSchema
from util.response_builder import ApiResponse


reset_blueprint_name = 'reset'
reset_route = Blueprint(reset_blueprint_name, __name__, url_prefix='/reset')


@reset_route.route('')
@marshal_with(PurchaseResponseSchema)
@doc(tags=['Reset'], description='''<pre>Endpoint to reset all tables in the database to its initial state</pre>''')
def reset_data():
    try:
        start_seed(db)
    except:
        return ApiResponse(message='Something wrong happened!', has_error=True).respond()
    return ApiResponse().respond()
