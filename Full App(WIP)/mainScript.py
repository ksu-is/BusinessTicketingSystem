from flask import Flask,redirect,render_template,request,url_for 
import mysql.connector

mydb = mysql.connector.connect( 
    host = "localhost", 
    user = "root", password = "", 
    database = "(your database name)" )

app = Flask(__name__) 
@app.route("/") 
def home(): 
    return render_template("index.html")
