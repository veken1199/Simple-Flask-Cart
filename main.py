from flask import Flask, jsonify, request, render_template, Markup
from flask_sessionstore import Session
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec

import os
from database import db
from api.product import product_route, get_product, get_products, product_blueprint_name
from api.purchase import purchase_route, purchase, purchase_blueprint_name
from api.cart import cart_route, cart, add_to_cart, delete_from_cart,cart_checkout, cart_blueprint_name
from api.reset import reset_route, reset_data, reset_blueprint_name


def create_app(config='config.BaseConfig'):
    app = Flask(__name__)
    app.config.from_object(config)
    app.app_context().push()

    session = Session(app)
    session.app.session_interface.db.create_all()
    db.init_app(app)

    app.register_blueprint(product_route)
    app.register_blueprint(purchase_route)
    app.register_blueprint(cart_route)
    app.register_blueprint(reset_route)

    return app, db


def create_docs(app):
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Shopify Challenge',
            version='v1',
            plugins=[MarshmallowPlugin()],
        ),
        'APISPEC_SWAGGER_URL': '/docs/',
    })
    docs = FlaskApiSpec(app)

    docs.register(get_product, blueprint=product_blueprint_name)
    docs.register(get_products, blueprint=product_blueprint_name)

    docs.register(purchase, blueprint=purchase_blueprint_name)

    docs.register(cart, blueprint=cart_blueprint_name)
    docs.register(add_to_cart, blueprint=cart_blueprint_name)
    docs.register(delete_from_cart, blueprint=cart_blueprint_name)
    docs.register(cart_checkout, blueprint=cart_blueprint_name)
    docs.register(reset_data, blueprint=reset_blueprint_name)
    return docs

app, _ = create_app()
docs = create_docs(app)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message':'These route is not valid...Try another'}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({'message': 'Something wrong happened! if this keeps happening, please considering '
                               'resetting using {}reset route'.format(request.url_root)}), 500


@app.errorhandler(405)
def method_not_valid(e):
    return jsonify({'message': 'The method is not valid for this route.... Try another'}), 405


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)