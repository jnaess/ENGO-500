import re
import os

from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
import requests

import pandas as pd
from shapely.geometry import Point
import pkg_resources
from geopandas import GeoDataFrame
import json

from flask_sqlalchemy import SQLAlchemy


from classes import *
from test_folder.test_script import printer

app = Flask(__name__)

# Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://mnonspcirnraqg:7919dd02f614cb83509e2889ec281800889dec45fb24c57db99d632e678f5626@ec2-52-3-60-53.compute-1.amazonaws.com:5432/d3kr6lkene46qr"

db = SQLAlchemy(app)

#db = SQL("postgres://mnonspcirnraqg:7919dd02f614cb83509e2889ec281800889dec45fb24c57db99d632e678f5626@ec2-52-3-60-53.compute-1.amazonaws.com:5432/d3kr6lkene46qr")           
            
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Main page
@app.route('/')
def index():
    printer()
    
    df1 = []
    
    df1 = db.execute("SELECT * FROM Simulations")
    
    print(df1)
    return render_template('index.html')

# Research and Development page
@app.route("/R_D")
def R_D():
    return render_template("R_D.html")

# Software Demo page
@app.route("/Software_Demo", methods=['POST', 'GET'])
def Software_Demo():

    df = pd.DataFrame({#'zip':[19152,19047],
                   'Lat':[40.058841,40.202162],
                   'Lon':[-75.042164,-74.924594]})

    geometry = [Point(xy) for xy in zip(df.Lon, df.Lat)]

    gdf = GeoDataFrame(df, geometry=geometry)

    geoJSON = gdf.to_json()
    geoJSON = json.loads(geoJSON)

    return render_template("Software_Demo.html", geoJSON = geoJSON)


# Loading page for Software Demo
@app.route("/loading", methods=['POST', 'GET'])
def loading():
    return render_template("loading.html")



if __name__ == "__main__":
    app.run()




