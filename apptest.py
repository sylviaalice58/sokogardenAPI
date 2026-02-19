# import flask and its components
from flask import *

# import the pymysql module - It helps us to create connection between python flask and mysql database
import pymysql

# NEW: import password hashing functions from werkzeug
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

        # NEW: Hash the password before storing
        hashed_password = generate_password_hash(password)

        # establish a connection between flask/python and mysql
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        # create a cursor to execute the sql queries
        cursor = connection.cursor()

        # structure an sql to insert the details received from the form
        # The %s is a placeholder -> A place holder it stands in places of actual values i.e we shall replace later on
        sql = "INSERT INTO users(username, email, phone, password) VALUES(%s, %s, %s, %s)"

        # create a tuple that will hold all the data gotten from the form
        # NEW: Use hashed_password instead of plain password
        data = (username, email, phone, hashed_password)

        # by use of the cursor, execute the sql as you replace the placeholder with the actual values
        cursor.execute(sql, data)

        # commit the changes to the database
        connection.commit()

        return jsonify({"message" : "User registered successfully"})


# Below is the login/sign in route
@app.route("/api/signin", methods=["POST"])
def signin():
    if request.method == "POST":
        # extract the two details entered on the form
        email = request.form["email"]
        password = request.form["password"]

        # create/establish a connection to the database
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        # create a cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # structure the sql query that will fetch the user by email only (we'll verify password later)
        sql = "SELECT * FROM users WHERE email = %s"

        # put the data received into a tuple
        data = (email,)

        # by use of the cursor execute the sql
        cursor.execute(sql, data)

        # fetch the user record if it exists
        user = cursor.fetchone()

        # NEW: Verify password using check_password_hash
        if user and check_password_hash(user['password'], password):
            # Login successful
            return jsonify({"message": "User logged in successfully", "user": user})
        else:
            # Login failed
            return jsonify({"message": "Login failed"})

# run the application 
app.run(debug=True)