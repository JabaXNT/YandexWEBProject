from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, render_template
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)


@app.route("/")
def index():
    return render_template('')


def main():
    db_session.global_init('db/products.db')
    app.run(debug=True)


if __name__ == '__main__':
    main()
