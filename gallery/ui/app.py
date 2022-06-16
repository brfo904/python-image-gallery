from flask import Flask
from flask import request, render_template, jsonify, redirect, flash, session
import json
from ..aws.session_secret import get_secret_flask_session
from gallery.data.db import *

from functools import wraps

app = Flask(__name__)
app.secret_key = get_secret_flask_session()
connect()
searchusers = "select * from users;"

@app.route('/')
def redirect_user():
    return redirect('/login')


@app.route('/<name>')
def homepage(name):
    return render_template('home.html', name=name)


# admin menu items
@app.route('/admin/users')
def main_menu():
    if not check_admin():
        return redirect('/login')
    u=get_session_username()
    return render_template('adminmenu.html', userlist=userlist(), name=u)


@app.route('/admin/listusers')
def list_users():
    return render_template('listusers.html')


@app.route('/admin/adduser')
def add_users():
    if not check_admin():
        return redirect('/login')
    return render_template('adduser.html')


@app.route('/admin/add_user_confirm', methods=['POST'])
def begin_add():
   if not check_admin():
       return redirect('/login')
   username = request.form['un0']
   pw = request.form['pw1']
   fname = request.form['fname2']
   if usercheck(username):
       return redirect('/admin')
   else: 
       user_add(username, pw, fname)
       return render_template('addeduserconfirm.html', name=fname)


@app.route('/admin/edituser/<name>', methods=['GET'])
def edit_user(name):
    if not check_admin():
        return redirect('/login')
    return render_template('edituser.html', name=name)


@app.route('/admin/edit_user_confirm/<name>', methods=['POST'])
def make_edit(name):
    if not check_admin():
        return redirect('/login')
    pw = request.form['pw']
    fname = request.form['fname']
    if pw != "":
        update_pw(name, pw)
    if fname != "":
        update_fname(name, fname)
    return redirect('/admin/edituser/' + name)


@app.route('/admin/deleteuser/<name>', methods=['GET'])
def delete_user(name):
    if not check_admin():
        return redirect('/login')
    return render_template('deleteuser.html', name=name)


@app.route('/admin/delete_user_confirm/<name>', methods=['POST'])
def delete_confirm(name):
    if not check_admin():
        return redirect('/login')    
    delete(name)
    return redirect('/admin/users')


#admin methods
def check_admin():
   username = get_session_username()
   confirm = is_admin(username)
   return confirm == 1


#user menus
@app.route('/users/<name>/viewimg', methods=['GET'])
def retrieve_images(name):
    u = get_session_username()
    return render_template('viewimg.html', name=u)


@app.route('/users/<name>/uploadimg', methods=['GET'])
def upload_images(name):
    u = get_session_username()
    return render_template('uploadimg.html', name=u)


@app.route('/users/processupload', methods=['POST'])
def process_upload():
    username = get_session_username()


#user methods
def get_session_username():
   return session['username']


#login pages
@app.route('/login', methods=['GET', 'POST'])
def login_screen():
    if request.method == 'POST':
        user = get_user(request.form["username"])
        if user is None or user.password != request.form["pwd"]:
            return redirect('/failedauth')
        else:
            session['username'] = request.form["username"]
            return redirect('/'+session['username'])
    else:
        return render_template('login.html')


@app.route('/failedauth')
def failed_auth():
    return render_template('failedlogin.html')

