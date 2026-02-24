# import flask and its components
from flask import *
import os
# import the pymysql module - It helps us to create connection between python flask and mysql database
import pymysql

# Create a flask application and give it a name
app = Flask(__name__) 

# configure the location to where your product images will be saved on your application
app.config["UPLOAD_FOLDER"] = "static/images"

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
        data = (username, email, phone, password)

        # by use of the cursor, execute the sql as you replace the placeholder with the actual values
        cursor.execute(sql, data)

        # commit the changes to the database
        connection.commit()


        return jsonify({"message" : "User registered successfully"})



# Below is the login/sign in route
@app.route("/api/signin",methods=["POST"])
def signin():
    if request.method =="POST":
        # extract the two details entered on the form
        email = request.form["email"]
        password = request.form["password"]

        # print out the details enteres
        # print(email, password)

        # create/establish  a connection to the database
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        # create a cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # structure the sql query that will check whether the email and password entered is correct
        sql ="SELECT * FROM users WHERE email = %s AND password = %s"

        # put the data received into a tuple
        data = (email, password)

        # by use of the cursor execute the sql
        cursor.execute(sql, data)

        # check whether there are rows returned and store the same on a variable
        count= cursor.rowcount
        # print(count) 

        # if there are record return it means the password and email are correct otherwise it means they are wrong 
        if count== 0:
            return jsonify({"message":"Login failed"}) 
        else:
            # There must be a user so we create a variable that will hold the details of the user fetched from the database
            user=cursor.fetchone()
            # Return the details to the frontend as well as a message
            return jsonify({"message":"User logged in successfully", "user":user})
        
# below is the route for adding products
@app.route("/api/add_product", methods = ["POST"])
def Addproduct():
    if request.method == "POST":
        # Extract the different details entered on the form
        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        product_cost = request.form["product_cost"]
        # for the product photo we shall fetch it from files as shown below
        product_photo = request.files["product_photo"]

        # extract the filename of the produc photo
        filename = product_photo.filename
        # print("This is the file name: ", filename)
        # by use of the os module (operating system) we can extract the file path where the images is currently saved
        photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # print("This is the photo path: ", photo_path)
        # save the product photo image into the new location
        product_photo.save(photo_path)

        # print them out to test whether younare recieving the details sent with the request
        # print(product_name, product_description, product_cost, product_photo)

        # establish a connection between flask/python and mysql
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        # create a cursor to execute the sql queries
        cursor = connection.cursor()

        # structure an sql to insert the details received from the form
        # The %s is a placeholder -> A place holder it stands in places of actual values i.e we shall replace later on
        sql = "INSERT INTO product_details(product_name, product_description, product_cost, product_photo) VALUES(%s, %s, %s, %s)"

        # create a tuple that will hold all the data gotten from the form which are currently held onto the different variables declared above
        data = (product_name, product_description, product_cost, filename)
        # by use of the cursor, execute the sql as you replace the placeholder with the actual values
        cursor.execute(sql, data)

        # commit the changes to the database
        connection.commit()




        return jsonify({"message": "Product added successfully"})

# BELOW IS THE ROUTE FOR FETCHING PRODUCT
@app.route("/api/get_products")

def get_products():
    # Create a connection to the data base
    connection=pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

    # create a cursor
    cursor=connection.cursor(pymysql.cursors.DictCursor)

    # structure the sql query that will fetch all the products from the database
    sql="SELECT * FROM product_details"

    # by use of the cursor execute the sql 
    cursor.execute(sql)

    # fetch all the products and store them in a variable
    products=cursor.fetchall() 


    return jsonify(products)

# Mpesa Payment Route/Endpoint 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
 
@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        amount = request.form['amount']
        phone = request.form['phone']
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"
 
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        # print("This is the responce given back: ", r)
 
        data = r.json()

        print("This is the content inside of variable data : ", data)

        access_token = "Bearer" + ' ' + data['access_token']
 
        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')
 
        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/api/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }
 
        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
 
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL
 
        response = requests.post(url, json=payload, headers=headers)
        print("This is tehe final response: ",response.text)
        return jsonify({"message": "Please Complete Payment in Your Phone and we will deliver in minutes"})



# run the application 
app.run(debug=True)