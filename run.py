# Colton Shoenberger, cs3585@drexel.edu
# CS530: DUI, Final Project

from flask import Flask, render_template, send_file, g, request, jsonify, session, escape, redirect, send_from_directory, url_for, make_response
from passlib.hash import pbkdf2_sha256
import os
from db import Database
from forms import Filters

app = Flask(__name__, static_folder='public', static_url_path='')
app.secret_key = b'cms69t&%$3rhfSwu3D'


## DB
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


## HOME PAGE
@app.route('/', methods=['GET', 'POST'])
def index():
    form = Filters(request.form)
    if request.method == 'POST' and form.validate():
        abvMin = request.form['abvMin']
        abvMax = request.form['abvMax']
        ibuMin = request.form['ibuMin']
        ibuMax = request.form['ibuMax']
        calMin = request.form['calMin']
        calMax = request.form['calMax']
    else :
        abvMin = 0
        abvMax = 30
        ibuMin = 0
        ibuMax = 120
        calMin = 0
        calMax = 400
    return render_template('index.html', form=form, abvMin=abvMin, abvMax=abvMax, ibuMin=ibuMin, ibuMax=ibuMax, calMin=calMin, calMax=calMax)

## BEER
@app.route('/api/beer', methods=['GET', 'POST'])
def api_beer():
    n = request.args.get('n', default=6)
    offset = request.args.get('offset', default=0)
    abvMin = request.args.get('abvMin', default=0)
    abvMax = request.args.get('abvMax', default=30)
    ibuMin = request.args.get('ibuMin', default=0)
    ibuMax = request.args.get('ibuMax', default=120)
    calMin = request.args.get('calMin', default=0)
    calMax = request.args.get('calMax', default=400)
    response = {
        'beer': get_db().get_beer(n, offset, abvMin, abvMax, ibuMin, ibuMax, calMin, calMax),
        'total': get_db().get_total_beer_count(abvMin, abvMax, ibuMin, ibuMax, calMin, calMax)
    }
    return jsonify(response)


## USERS
@app.route('/api/users')
def api_users():
    n = request.args.get('n', default=6)
    offset = request.args.get('offset', default=0)
    response = {
        'user': get_db().get_users(n, offset),
        'total': get_db().get_total_user_count()
    }
    return jsonify(response)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        typed_password = request.form['password']
        if name and username and typed_password:
            encrypted_password = pbkdf2_sha256.encrypt(typed_password, rounds=200000, salt_size=16)
            get_db().create_user(name, username, encrypted_password)
            return redirect('/login')
    return render_template('create_user.html')


## LOGIN / LOGOUT

# Check if user is logged in
#
# @app.route('/api/check_login', methods=['GET', 'POST'])
# def check_login():
#     if 'user' in session:
#         return True
#     else:
#         return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        typed_password = request.form['password']
        if username and typed_password:
            user = get_db().get_user(username)
            if user:
                if pbkdf2_sha256.verify(typed_password, user['encrypted_password']):
                    session['user'] = user
                    return redirect('/')
                else:
                    message = "Incorrect password, please try again"
            else:
                message = "Unknown user, please try again"
        elif username and not typed_password:
            message = "Missing password, please try again"
        elif not username and typed_password:
            message = "Missing username, please try again"
    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


# FAVORITES
@app.route('/api/add_favorite', methods=['GET', 'POST'])
def api_add_favorite():
    if 'user' in session:
        user_id = session['user']['uid']
        beer_id = request.args.get('uid')
        get_db().add_favorite(user_id, beer_id)
    return api_beer()

@app.route('/api/unfavorite')
def api_unfavorite():
    if 'user' in session:
        user_id = session['user']['uid']
        beer_id = request.args.get('uid')
        get_db().unfavorite(user_id, beer_id)
        return api_my_favorites()
    else:
        return jsonify('Error: User not authenticated')

@app.route('/api/my_favorites')
def api_my_favorites():
    if 'user' in session:
        user_id = session['user']['uid']
        n = request.args.get('n', default=6)
        offset = request.args.get('offset', default=0)
        response = {
            'beer': get_db().my_favorites(user_id, n, offset),
            'total': get_db().get_my_favorites_count(user_id)
        }
        return jsonify(response)
    else:
        return jsonify('Error: User not authenticated')

@app.route('/api/favorites')
def api_favorites():
    n = request.args.get('n', default=6)
    offset = request.args.get('offset', default=0)
    response = {
        'user': get_db().get_favorites(n, offset),
        'total': get_db().get_total_favorites_count()
    }
    return jsonify(response)


# Handle any unhandled filename by loading its template
@app.route('/<name>')
def generic(name):
        return render_template(name + '.html')


# INIT
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8148, debug=False)