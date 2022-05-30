import psycopg2

db_host = "development-db1.c33oyac2tqvj.us-east-1.rds.amazonaws.com"
db_name = "image_gallery"
db_user = "image_gallery"

password_file = "/home/ec2-user/.image_gallery_config"

connection = None


def get_menu():
    menu = "1)\tList users\n2)\tAdd User\n3)\tEdit user\n4)\tDelete user\n5)\tQuit"
    print(menu)
    option = int(input("Enter your command: "))
    while option != 5:
        if option == 1:
            print("to come")
            get_menu()
        elif option == 2:
            print("to come")
            get_menu()
        elif option == 3:
            print("to come")
            get_menu()
        elif option == 4:
            print("to come")
            get_menu()
        else:
            print("Invalid selection. Try again!")
            get_menu()

    print("Bye!")
    exit()


def get_password():
    f = open(password_file, "r")
    result = f.readline()
    f.close()
    return result[:-1]


def connect():
    global connection
    connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())


def execute(query):
    global connection
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor


def main():
    connect()
    res = execute('select * from users')
    for row in res:
        print(row)


if __name__ == '__main__':
    main()
    
