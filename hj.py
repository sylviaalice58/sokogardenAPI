# import flask and its components
from flask import *

# import the pymysql module - It helps us to create connection between python flask and mysql database
import pymysql

# import password hashing functions
from werkzeug.security import generate_password_hash, check_password_hash

# Create a flask application and give it a name
app = Flask(__name__) 


# below is the sign up route 
@app.route("/api/signup", methods = ["POST"])
def signup():
    if request.method=="POST":
        # Extract the different details entered on the form 
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        # by use of the print function lets print all those details sent with the upcoming request
        # print(username, email, password, phone)

        # establish a connection between flask/python and mysql
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        # create a cursor to execute the sql queries
        cursor = connection.cursor()

        # structure an sql to insert the details received from the form
        # The %s is a placeholder -> A place holder it stands in places of actual values i.e we shall replace later on
        sql = "INSERT INTO users(username,email,phone,password) VALUES(%s, %s, %s, %s)"

        # create a tuple that will hold all the data gotten from the form
        # hash the password before storing it
        data = (username, email, phone, generate_password_hash(password))

        # by use of the cursor, execute the sql as you replace the placeholder with the actual values
        cursor.execute(sql, data)

        # commit the changes to the database
        connection.commit()


        return jsonify({"message" : "User registered successfully"})



@app.route("/api/signin", methods=["POST"])

def signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form.get("password")

        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = "SELECT * FROM users WHERE email = %s"
        cursor.execute(sql,  (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            # Login successful – remove password before sending
            del user['password']
            return jsonify({"message": "User logged in successfully", "user": user})
        else:
            return jsonify({"message": "Login failed"})
app.run(debug=True)