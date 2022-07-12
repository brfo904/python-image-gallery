import os, json

from flask import Flask
from flask import request, render_template, jsonify, redirect, flash, session, send_from_directory

from ..aws.session_secret import get_secret_flask_session
from ..aws.s3 import create_bucket, put_object, upload_file, download_file, delete_file
from gallery.data.db import *

from functools import wraps
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SESSION_SECRET')
app.config['UPLOAD_FOLDER'] = 'gallery/ui/static/project/uploads'
DOWNLOAD_FOLDER = '/home/ec2-user/python-image-gallery/gallery/ui/static/project/images'
connect()
ALLOWED_EXTENSIONS = {'gif', 'jpg', 'jpeg', 'png'}


@app.route('/')
def homepage():
    if not (logged_in()):
        return redirect('/login')
    first_name = get_session_first_name()
    return render_template('home.html')


# admin menu items
@app.route('/admin/users')
def main_menu():
    if not check_admin():
        logout()
        return redirect('/login')
    first_name = get_session_first_name()
    return render_template('adminmenu.html', userlist=userlist())


@app.route('/admin/listusers')
def list_users():
    return render_template('listusers.html')


@app.route('/admin/adduser')
def add_users():
    if not check_admin():
        logout()
        return redirect('/login')
    return render_template('adduser.html')


@app.route('/admin/add_user_confirm', methods=['POST'])
def begin_add():
   if not check_admin():
       logout()
       return redirect('/login')
   username = request.form['un0']
   pw = request.form['pw1']
   fname = request.form['fname2']
   is_admin = request.form['admin']
   if usercheck(username):
       flash('User with username: ' + username + ' already exists!')
       return redirect('/admin/adduser')
   else: 
       user_add(username, pw, fname, is_admin)
       flash(fname + ' has been created!')
       return redirect('/admin/adduser')


@app.route('/admin')
def logout_admin():
    return redirect('/admin/users')


@app.route('/admin/edituser/<name>', methods=['GET'])
def edit_user(name):
    if not check_admin():
        logout()
        return redirect('/login')
    return render_template('edituser.html', name=name)


@app.route('/admin/edit_user_confirm/<name>', methods=['POST'])
def make_edit(name):
    if not check_admin():
        logout()
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
        logout()
        return redirect('/login')
    return render_template('deleteuser.html', name=name)


@app.route('/admin/delete_user_confirm/<name>', methods=['POST'])
def delete_confirm(name):
    if not check_admin():
        logout()
        return redirect('/login')
    delete(name)
    return redirect('/admin/users')


#admin methods
def check_admin():
   username = get_session_username()
   confirm = is_admin(username)
   return confirm == 1


#user menus
@app.route('/users/viewimg')
def view_images():
    if not (logged_in()):
        return redirect('/login')
    u = get_session_username()
    images = get_image_list(u)
    bucket = get_upload_path()
    for image in images:
        key = get_session_username()+'/uploads/'+image.file_name
        download_file(bucket, key, image.file_name)
        os.system(f'mv {image.file_name} gallery/ui/static/project/images/')
    return render_template('viewimg.html', imagelist=images)


@app.route('/users/uploadimg', methods=['GET'])
def upload_images():
    if not (logged_in()):
        return redirect('/login')
    user = get_session_username()
    return render_template('uploadimg.html', username=user)


@app.route('/users/processupload', methods=['POST'])
def process_upload():
    if not (logged_in()):
        return redirect('/login')
    if 'file' not in request.files:
        flash('Issue with file. Try again!')
        return redirect('/users/uploadimg')
    image = request.files['file']
    if image.filename == '':
        flash('No file uploaded!')
        return redirect('/users/uploadimg')
    if image and allowed_file(image.filename):
        imagename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename))
        bucket = get_upload_path()
        upload_file(app.config['UPLOAD_FOLDER'] + '/' + imagename, bucket, request.form["key"]+image.filename)
        store_filename(get_session_username(), imagename)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], imagename))
        flash('File uploaded.')
        return redirect('/users/uploadimg')


@app.route('/users/invalidupload')
def invalid_upload():
    return(render_template('invalidupload.html'))


@app.route('/users')
def redirect_user():
    return redirect('/')


@app.route('/static/project/downloads/<image_name>')
def send_file(image_name):
    try:
        return send_from_directory(DOWNLOAD_FOLDER, image_name, as_attachment=False)
    except FileNotFoundError:
        print('File not found!')


@app.route('/users/deleteimg/<image_name>')
def delete_image(image_name):
    img = get_image(image_name, get_session_username())
    if img is None:
        flash('Image not found in Database!')
        return redirect('/users/viewimg')
    bucket = get_upload_path()
    key = get_session_username()+'/uploads/'+img.file_name
    delete_file(bucket, key)
    remove_filename(get_session_username(), img.file_name, img.id)
    flash('Image: ' + img.file_name + ' deleted.')
    return redirect('/users/viewimg')


#user methods
def get_session_username():
    return session['username']


def get_session_first_name():
    logged_user = get_user(get_session_username())
    first_name = logged_user.full_name.split(" ")
    return first_name[0].title()


def logged_in():
    if (session.get('user_id') is None):
        return False
    return True 


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_download_path():
    path = 'edu.au.cc.b0rk-image-gallery.'+get_session_username()+'.uploads'
    return path


def get_upload_path():
    path = 'edu.au.cc.b0rk-image-gallery'
    return path


#login pages
@app.route('/login', methods=['GET', 'POST'])
def login_screen():
    if request.method == 'POST':
        user = get_user(request.form["user"])
        if user is None or user.password != request.form["pwd"]:
            return redirect('/failedauth')
        else:
            session['username'] = request.form["user"]
            return redirect('/')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
   session["username"] = None
   return redirect('/')


@app.route('/failedauth')
def failed_auth():
    return render_template('failedlogin.html')


