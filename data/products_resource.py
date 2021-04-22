from data.products import Product
from data import db_session
from flask import Flask, abort, json, jsonify
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('title', required=True, type=str)
parser.add_argument('content', required=True)
parser.add_argument('count', required=True, type=str)


class ProductsResource(Resource):
    def get(self, product_id):
        abort_if_news_not_found(product_id)
        session = db_session.create_session()
        return jsonify()

    def delete(self, product_id):
        abort_if_news_not_found(product_id)
        session = db_session.create_session()
        product = session.query(Product).get(product_id)
        session.delete(product)
        session.commit()
        return jsonify({'success': 'OK'})


class ProductsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        product = session.query(Product).all()
        return jsonify(
            {
                'product':
                [item.to_dict(only=('id', 'title', 'content', 'count'))
                 for item in product]
            }
        )

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        product = Product(
            title=args['title'],
            content=args['content'],
            count=args['count'],
        )
        session.add(product)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_news_not_found(product_id):
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    if not product:
        abort(404, message=f"product {product_id} not found")
