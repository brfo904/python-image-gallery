from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/admin')
def main_menu():
    return render_template('adminmenu.html')


@app.route('/admin/listusers')
def list_users():
    return render_template('listusers.html')


@app.route('/admin/adduser')
def add_users():
    return render_template('adduser.html')


@app.route('/admin/edituser')
def edit_user():
    return render_template('edituser.html')


@app.route('/admin/deleteuser')
def delete_user():
	return render_template('deleteuser.html')

