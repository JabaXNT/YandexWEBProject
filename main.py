from flask import Flask, render_template, request, redirect, session, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_restful import Api
from data.user import User
from data.products import Product
from forms.reg_user import RegisterForm
from forms.login_user import LoginForm
from data import db_session
from data import users_resource, products_resource
import json
import ast

app = Flask(__name__)
app.add_template_global(ast.literal_eval, name='dict')
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
    session['is_admin'] = None
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            session['login'] = str(user)
            session['is_admin'] = str(user.is_admin)
            session['favorite'] = []
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
        only=('id', 'title', 'count', 'price', 'image'))}
    return render_template('products.html', list_product=list_product)


@app.route('/bin', methods=['GET', 'POST'])
@login_required
def bin():
    db_sess = db_session.create_session()
    bin_sess = db_sess.query(User).get(current_user.id)
    bin_list = {'product': bin_sess.to_dict(
        only=('bin',))}
    bin_list = bin_list['product']
    return render_template('bin.html', list_product=bin_list)


@app.route('/fav')
@login_required
def fav():
    db_sess = db_session.create_session()
    fav_sess = db_sess.query(User).get(current_user.id)
    fav_list = {'product': fav_sess.to_dict(
        only=('favourite',))}
    return render_template('fav.html', list_product=fav_list)


@app.route('/add_bin', methods=['GET', 'POST'])
@login_required
def bin_add():
    db_sess = db_session.create_session()
    product_id_bin = str(json.loads(request.data)['id'])
    product_count_bin = str(json.loads(request.data)['count'])
    user = db_sess.query(User).filter(
        User.username == current_user.username).first()
    product = db_sess.query(Product).get(product_id_bin)
    inter = ast.literal_eval(user.bin)
    list_product = {'product': product.to_dict(
        only=('id', 'title', 'count', 'price'))}
    list_product['product']['count'] = product_count_bin
    if list_product in inter:
        print(inter.index[list_product['product']['title']])
        return {'200': 'Accept'}
    inter.append(list_product)
    user.bin = str(inter)
    db_sess.commit()
    return {'200': 'Accept'}


@app.route('/add_favourite', methods=['GET', 'POST'])
@login_required
def favourite_add():
    db_sess = db_session.create_session()
    product_id_fav = str(json.loads(request.data)['id'])
    product_count_fav = str(json.loads(request.data)['count'])
    user = db_sess.query(User).filter(
        User.username == current_user.username).first()
    product = db_sess.query(Product).get(product_id_fav)
    inter = ast.literal_eval(user.favourite)
    list_product = {'product': product.to_dict(
        only=('id', 'title', 'count', 'price', 'image'))}
    list_product['product']['count'] = product_count_fav
    if list_product in inter:
        return {'200': 'Accept'}
    inter.append(list_product)
    user.favourite = str(inter)
    db_sess.commit()
    return {'200': 'Accept'}


@app.route('/del_fav')
@login_required
def del_fav():
    db_sess = db_session.create_session()
    product_id_fav = str(json.loads(request.data)['id'])
    user = db_sess.query(User).filter(
        User.username == current_user.username).first()
    inter = ast.literal_eval(user.favourite)
    for i in range(len(inter)):
        if product_id_fav == inter[i]['product']['id']:
            del inter[i]
    user.favourite = str(inter)
    db_sess.commit()
    return {'200': 'Accept'}


@app.route('/del_bin')
@login_required
def del_bin():
    db_sess = db_session.create_session()
    product_id_bin = str(json.loads(request.data)['id'])
    user = db_sess.query(User).filter(
        User.username == current_user.username).first()
    inter = ast.literal_eval(user.bin)
    for i in range(len(inter)):
        if product_id_bin == inter[i]['product']['id']:
            del inter[i]
    user.bin = str(inter)
    db_sess.commit()
    return {'200': 'Accept'}


@app.route('/edit_product', methods=['POST'])
@login_required
def edit_bin():
    db_sess = db_session.create_session()
    product_data = json.loads(request.data)['content']
    product = db_sess.query(Product).filter(
        Product.id == product_data['id']).first()
    product.title = product_data['title']
    product.price = product_data['price']
    product.count = product_data['count']
    db_sess.commit()
    return {'200': 'Accept'}


@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    db_sess = db_session.create_session()
    product_data = json.loads(request.data)['content']
    product = Product(
        title=product_data['title'],
        price=product_data['price'],
        count=product_data['count'],
    )
    db_sess.add(product)
    db_sess.commit()
    return {'200': 'Accept'}


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session['login'] = None
    return redirect("/")


def main():
    db_session.global_init('db/products_final.db')
    app.run(host='127.0.0.1', port='5000', debug=True)


if __name__ == '__main__':
    main()
