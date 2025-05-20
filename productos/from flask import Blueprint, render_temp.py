from flask import Blueprint, render_template, redirect, request, url_for, flash

from flask_login import login_user, login_required, logout_user

from ..models.models import User, Product

from .. import db, login_manager

from werkzeug.security import check_password_hash

 

main = Blueprint('main', __name__)

 

@login_manager.user_loader

def load_user(user_id):

   return User.query.get(int(user_id))

 

@main.route('/', methods=['GET', 'POST'])

def login():

   if request.method == 'POST':

       user = User.query.filter_by(username=request.form['username']).first()

       if user and check_password_hash(user.password, request.form['password']):

           login_user(user)

           return redirect(url_for('main.dashboard'))

       flash('Login incorrecto')

   return render_template('login.html')

 

@main.route('/dashboard')

@login_required

def dashboard():

   return render_template('dashboard.html')

 

@main.route('/logout')

@login_required

def logout():

   logout_user()

   return redirect(url_for('main.login'))

 

@main.route('/product/create', methods=['GET', 'POST'])

@login_required

def create_product():

   if request.method == 'POST':

       product = Product(

           name=request.form['name'],

           quantity=int(request.form['quantity']),

           price=float(request.form['price'])

       )

       db.session.add(product)

       db.session.commit()

       return redirect(url_for('main.inventory'))

   return render_template('create_product.html')

 

@main.route('/inventory')

@login_required

def inventory():

   products = Product.query.all()

   return render_template('inventory.html', products=products)

 

@main.route('/sales')

@login_required

def sales():

   return render_template('sales.html')

 

@main.route('/receptions')

@login_required

def receptions():

   return render_template('receptions.html')