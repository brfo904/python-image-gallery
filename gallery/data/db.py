import os
import psycopg2
import json
from gallery.aws.secrets import get_secret_image_gallery
from gallery.data.user import User
from gallery.data.image import Image

db_name = "image_gallery"
connection = None

def get_secret():
    return None


def get_password():
    file = open("/mnt/data/imagegallery")
    result = file.readline().strip()
    file.close()
    return result

def get_host():
    host = os.getenv('PG_HOST')
    return host


def get_username():
    user = os.getenv('IG_USER')
    return user


def get_dbname():
    db = os.getenv('IG_DATABASE')
    return db


def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(), dbname=get_dbname(), user=get_username(), password=get_password())
    connection.set_session(autocommit=True)

def execute(query, args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

#admin user methods
def userlist():
   connect()
   search = 'select * from users;'
   users = execute(search)
   userlist = []
   for row in users:
       userlist.append({'name':row[2], 'username':row[0]})
   return userlist


def update_pw(username, pw):
   connect()
   pw_update = "update users set password =(%s) where username=(%s);"
   results = execute(pw_update, (pw, username))


def update_fname(username, full_name):
   connect()
   fname_update = "update users set full_name =(%s) where username=(%s);"
   results = execute(fname_update, (full_name, username))


def delete(username):
   connect()
   delete = "delete from users where username=(%s);"
   results = execute(delete, (username,))


def usercheck(username):
   connect()
   checker = "select * from users where username=(%s);"
   results = execute(checker, (username,))
   return(results.rowcount > 0)


def user_add(username, pword, fname, admin):
   connect()
   add = "INSERT INTO users (username, password, full_name, isAdmin) VALUES (%s, %s, %s, %s);"
   results = execute(add, (username, pword, fname, admin,))


def get_user(username):
   connect()
   user_search = "select * from users where username=(%s);"
   results = execute(user_search, (username,))
   row = results.fetchone()
   if row is None:
      return None
   else:
      return User(row[0], row[1], row[2])


def is_admin(username):
   connect()
   check = "select * from users where username=(%s) AND isAdmin=1;"
   results = execute(check, (username,))
   row = results.fetchone()
   if row is None:
      return 0
   else:
      return 1


#user methods
def store_filename(owner, file):
    connect()
    store = "insert into images(owner, file, upload_date) values (%s, %s, NOW())"
    results = execute(store, (owner, file,))


def remove_filename(owner, file, id):
    connect()
    remove = "delete from images where owner=(%s) AND file=(%s) AND image_id=(%s)"
    results = execute(remove, (owner, file, id,))


def get_image_list(owner):
   connect()
   images = "select file, owner, image_id from images where owner=(%s)"
   results = execute(images, (owner,))
   image_list = []
   for row in results:
       img = Image(row[0], row[1], row[2])
       image_list.append(img)
   return image_list


def get_image(filename, owner):
   connect()
   image = "select file, owner, image_id from images where owner=(%s) and file=(%s)"
   results = execute(image, (owner, filename,))
   row = results.fetchone()
   if row is None:
      return None
   else:
      return Image(row[0], row[1], row[2])


def main():
   connect()
   images = "select file, owner from images where owner='barney'"
   results = execute(images)
   image_list = []
   for row in results:
       img = Image(row[0], row[1])
       image_list.append(img)
   for image in image_list:
        print(image.file_name + '\n')


if __name__ == '__main__':
    main()
    
