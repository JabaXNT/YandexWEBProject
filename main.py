from flask import Flask, render_template, request, redirect, session
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_restful import Api
from data.user import User
from data.products import Product
from forms.reg_user import RegisterForm
from forms.login_user import LoginForm
from data import db_session
from data import users_resource, products_resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
api.add_resource(products_resource.ProductsListResource, '/api/products')
api.add_resource(products_resource.ProductsResource,
                 '/api/products/<int:product_id>')
api.add_resource(users_resource.UserListResource, '/api/users')
api.add_resource(users_resource.UserResource, '/api/users/<int:user_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template('main.html', session=session)


@app.route('/reg', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            username=form.username.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    session['login'] = None
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            session['login'] = str(user)
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/products/<int:id_products>')
def product(id_products):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).get(id_products)
    list_product = {'product': product.to_dict(
            only=('title', 'count', 'content', 'image'))}
    return render_template('products.html', list_product=list_product)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init('db/products_final.db')
    app.run(host='127.0.0.1', port='5000', debug=True)


if __name__ == '__main__':
    main()
