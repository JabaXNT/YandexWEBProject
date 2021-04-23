from flask_restful import Api
from flask import Flask, render_template, request, jsonify
from flask_jwt_simple import JWTManager, create_jwt, get_jwt_identity, jwt_required
from data import db_session
from data import users_resource, products_resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['JWT_SECRET_KEY'] = 'yandexlyceum_secret_key'
app.jwt = JWTManager(app)
api = Api(app)
api.add_resource(products_resource.ProductsListResource, '/products')
api.add_resource(products_resource.ProductsResource,
                 '/products/<int:product_id>')
api.add_resource(users_resource.UserListResource, '/users')
api.add_resource(users_resource.UserResource, '/users/<int:user_id>')


@app.route("/")
def index():
    return render_template('main.html')


def main():
    db_session.global_init('db/products.db')
    app.run(host='127.0.0.1', port='5000', debug=True)


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=username)}
    return jsonify(ret), 200


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    return jsonify({'hello_from': get_jwt_identity()}), 200


if __name__ == '__main__':
    main()
