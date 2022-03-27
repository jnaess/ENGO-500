import re
import os

from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
import requests

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Main page
@app.route('/')
def index():
    return render_template("index.html")

# Research and Development page
@app.route("/R_D")
def R_D():
    return render_template("R_D.html")

@app.route("/Software_Demo")
def Software_Demo():
    return render_template("Software_Demo.html")




