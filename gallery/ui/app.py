from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    return 'welcome home'


@app.route('/admin/usermenu')
def menu():
    return get_menu()


@app.route('/admin')
def main_menu():
    return 'sup? this will be the admin menu.'


@app.route('/admin/userlist')
def list_users():
    return 'this will list the users'


@app.route('/admin/adduser')
def add_user():
    return 'this will add users'


@app.route('/admin/edituser')
def edit_user():
    return 'this will edit user'


@app.route('/admin/deleteuser')
def delete_user():
    return 'this will delete user'


def get_menu():
    menu = """
<!DOCTYPE html>
<html>
  <head>
   <title>Image Gallery User Menu</title>
   <meta charset="utf-8" />
  </head>
  <body>
   <p>Hello</p>
  </body>
</html>"""
    return menu
