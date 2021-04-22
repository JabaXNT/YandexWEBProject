from flask_restful import Api
from flask import Flask, render_template
from data import db_session
from data import users_resource, products_resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
api.add_resource(products_resource.ProductsListResource, '/products')
api.add_resource(products_resource.ProductsResource,
                 '/products/<int:product_id>')
api.add_resource(users_resource.UserListResource, '/products/users')
api.add_resource(users_resource.UserResource, '/products/<int:user_id>')


@app.route("/")
def index():
    return render_template('main.html')


def main():
    db_session.global_init('db/products.db')
    app.run(host='127.0.0.1', port='5000', debug=True)


if __name__ == '__main__':
    main()
