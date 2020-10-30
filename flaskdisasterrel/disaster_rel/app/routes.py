from app import app
from app.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import current_user, login_user
from app.models import User, Post, Item , Donate
from flask_login import logout_user
from flask_login import login_required
from app import db
from flask import request
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    post_objs = Post.query.all()
    posts = []

    for post in post_objs:
        '''
        post_dict = {}
        user_id = post.user_id
        user = User.query.filter_by(id=user_id).first()
        post_dict['author'] = {'username': user.username}
        post_dict['post_body'] = {'post_body': post.body}
        post_dict['post_id'] = post.id
        '''
        posts.append(post)
    
    user_type = current_user.user_type
    '''
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    '''
    return render_template("index.html", title='Home Page', posts=posts, user_type=\
        user_type)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,user_type=form.user_type.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/_delete_post')#this can be done only by admin
def delete_post():
    post_id = request.args.get('post_id', 0, type=int)
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    donates = Donate.query.filter_by(post_id = post_id)
    for i in donates:
        db.session.delete(i)
        db.session.commit()

    print ('delete_post ', post_id)
    return jsonify(result='post deleted')

@app.route('/_create_post')#this can be done only by admin
def create_post():
    disaster_title = request.args.get('disaster_title')
    disaster_description = request.args.get('disaster_description')
    print ('title = ', disaster_title)
    print ('disaster_description = ', disaster_description)
    u = User.query.get(1)
    p = Post(title=disaster_title, body=disaster_description, author=current_user)
    db.session.add(p)
    db.session.commit()
    #I = Item(post_id=p.id,author=current_user)
    #db.session.add(I)
    #db.session.commit()
    post = {'id':p.id, 'title':disaster_title, 'body':disaster_description,
    'author':current_user.username, 'timestamp':p.timestamp}
    #print
    #db.session.delete(post)
    #db.session.commit()
    return jsonify(post=post)

@app.route('/post<post_id>',methods=['GET', 'POST'])
def post(post_id):
    p = Post.query.filter_by(id=post_id).first()
    i = Item.query.filter(Item.post_id==post_id).all()
    #for i in i:
    #    print(i.post_id, i.quantity, i.name)
    u = User.query.all()
    dic_item = {}
    for item in i:
        dic_item[item.id] = item.name
    dic_user = {}
    for item in u:
        dic_user[item.id] = item.username
    donates = Donate.query.filter_by(post_id=post_id).all()
    for item in donates:
        item.item_id = dic_item[item.item_id]
        item.donor_id = dic_user[item.donor_id]
    #donate = (donor,item_name,quantity,timestap)

    return render_template('post.html',post=p,items=i,donates = donates)
    #return jsonify(post=p)

@app.route('/_create_item')#this can be done only by admin
def create_item():
    item_name = request.args.get('item_name')
    item_quantity = request.args.get('item_quantity')
    item_unit = request.args.get('item_unit')
    post_id = request.args.get('post_id')
    print ('name = ', item_name)
    print ('item_quantity = ', item_quantity)
    #u = User.query.get(1)
    #p = Post(title=disaster_title, body=disaster_description, author=current_user)
    #db.session.add(p)
    #db.session.commit()
    I = Item(post_id = post_id, name=item_name,quantity=item_quantity,unit = item_unit)
    print(I.post_id)
    print(I.name)
    db.session.add(I)
    db.session.commit()
    #print(111111111)
   # post = {'id':p.id, 'title':disaster_title, 'body':disaster_description,
   # 'author':current_user.username, 'timestamp':p.timestamp}
    #db.session.delete(post)
    #db.session.commit()
    item = {'post_id': post_id,'name':item_name,'quantity':item_quantity,'item_id':I.id,'unit':I.unit}

    return jsonify(Item = item)


@app.route('/_delete_item')#this can be done only by admin
def delete_item():
    item_id = request.args.get('item_id', 0, type=int)
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    print ('delete_post ', item_id)
    return jsonify(result='item deleted')

@app.route('/_donate_item',methods=['GET', 'POST'])
def donate_item():
    print('do you get me?')
    item_id = request.args.get('item_id',0,type=int)
    donate_quantity = request.args.get('quantity',0,type=int)
    donor_id = request.args.get('donor_id',0,type=int)
    item = Item.query.get(item_id)
    post_id = item.post_id
    old_quantity = item.quantity
    item.quantity = old_quantity - donate_quantity
    db.session.commit()
    donate = Donate(post_id = post_id,item_id = item_id, donor_id = donor_id, quantity = donate_quantity)
    db.session.add(donate)
    #print(donate)

    db.session.commit()
   # print(donate.post_id, donate.item_id, donate.quantity,donate.id)

    donates = Donate.query.filter_by(post_id=post_id).all()
    item_name = Item.query.filter_by(id=item_id).first().name
    donor_name = User.query.filter_by(id=donor_id).first().username
    d = {'post_id':post_id,'donor_name':donor_name,'item_id':item_id,'donor_id':donor_id,'quantity':donate_quantity,'item_name':item_name,'id':donor_id}
    #print(new_quantity)

    return jsonify(result='item updated',donate=d)
"""
donate = Donate.query.all()
for i in donate:
    db.session.delete(i)
    db.session.commit()


ep = Donate.query.filter_by(item_id=51).all()

for i in ep:
    print(i.id,i.post_id,i.item_id)
    db.session.delete(i)
    db.session.commit()


with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('create_post'))
    users = User.query.all()
    for i in users:
        print(i.id,i.username,i.user_type)
    posts = Post.query.all()
    for i in posts:
        print(i.id,i.user_id,i.title)
    items = Item.query.all()
    for i in items:
        print(i.id,i.name,i.post_id,i.quantity)

    donates = Donate.query.all()
    for i in donates:
        print(i.id,i.post_id,i.item_id,i.donor_id,i.quantity)
        print(1)

item = Item.query.get(51)
item.quantity = 3
db.session.commit()
print(item.quantity)
"""
