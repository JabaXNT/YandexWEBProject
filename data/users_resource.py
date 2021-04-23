from data.user import User
from data import db_session
from flask import Flask, abort, jsonify
from flask_jwt_simple import jwt_required
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('surname', required=True, type=str)
parser.add_argument('name', required=True, type=str)
parser.add_argument('email', required=True, type=str)
parser.add_argument('hashed_password', required=True, type=str)


class UserResource(Resource):
    @jwt_required
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'surname', 'name', 'email', 'hashed_password'))})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        news = session.query(User).get(user_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify(
            {
                'user':
                [item.to_dict(only=('id', 'surname', 'name', 'email', 'hashed_password'))
                 for item in user]
            }
        )

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            email=args['email'],
        )
        user.set_password(args['hashed_password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_news_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
