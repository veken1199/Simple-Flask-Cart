from flask import Flask, jsonify, request
from flask_sessionstore import Session
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from api.product import *
from api.purchase import *
from api.cart import *

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.app_context().push()

    session = Session(app)
    session.app.session_interface.db.create_all()
    db.init_app(app)
    return app, db


def create_doc(app):
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Shopify Challenge',
            version='v1',
            plugins=[MarshmallowPlugin()],
        ),
        'APISPEC_SWAGGER_URL': '/docs/',
    })
    docs = FlaskApiSpec(app)
    return docs

app,_ = create_app()
docs = create_doc(app)

app.register_blueprint(product_route)
app.register_blueprint(purchase_route)
app.register_blueprint(cart_route)

docs.register(get_product, blueprint=product_blueprint_name)
docs.register(get_products, blueprint=product_blueprint_name)
docs.register(purchase, blueprint=purchase_blueprint_name)
docs.register(cart, blueprint=cart_blueprint_name)
docs.register(post_cart, blueprint=cart_blueprint_name)

# Now point your browser to localhost:5000/api/docs/
@app.route('/', methods=['POST'])
def post_user():
    data = request.get_json(force=True)
    data, errors = user_schema.load(data)
    print(data)
    print (errors)
    return jsonify({})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
