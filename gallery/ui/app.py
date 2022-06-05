from flask import Flask
from flask import request, render_template, jsonify, redirect
import json
from gallery.tools.db import *

app = Flask(__name__)
connect()
searchusers = "select * from users;"


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/admin')
def main_menu():
    return render_template('adminmenu.html', userlist=userlist())


@app.route('/admin/listusers')
def list_users():
    return render_template('listusers.html')


@app.route('/admin/adduser')
def add_users():
    return render_template('adduser.html')


@app.route('/admin/edituser/<name>', methods=['GET'])
def edit_user(name):
    return render_template('edituser.html', name=name)


@app.route('/admin/edit_user_confirm/<name>', methods=['POST'])
def make_edit(name):
    pw = request.form['pw']
    fname = request.form['fname']
    if pw != "":
        update_pw(name, pw)
    if fname != "":
        update_fname(name, fname)
    return redirect('/admin/edituser/' + name)


@app.route('/admin/deleteuser')
def delete_user():
	return render_template('deleteuser.html')


def main():
    x=[]
    connect()
    testing = execute('select * from users')
    for row in testing:
        x.append('name:' + row[2] + ', username:' + row[0])
    print(json.dumps(x))

if __name__=="__main__":
    main()
