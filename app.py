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

import psycopg2
from sqlalchemy import create_engine

from cs50 import SQL
#from flask_sqlalchemy import SQLAlchemy


from classes import *
from reports import reporter

app = Flask(__name__)

# Configure Database
db = SQL("postgresql://mnonspcirnraqg:7919dd02f614cb83509e2889ec281800889dec45fb24c57db99d632e678f5626@ec2-52-3-60-53.compute-1.amazonaws.com:5432/d3kr6lkene46qr") 

#db = SQLAlchemy(app)

#db = SQL("postgresql://mnonspcirnraqg:7919dd02f614cb83509e2889ec281800889dec45fb24c57db99d632e678f5626@ec2-52-3-60-53.compute-1.amazonaws.com:5432/d3kr6lkene46qr") 

#db = SQL("postgres://tdordoxeldwmqu:8f5dd3c7322b6a83fa9279eb76cdc139979adcc7b3c03ace597bac1661d1e696@ec2-34-239-196-254.compute-1.amazonaws.com:5432/dal40v64r9dbnv")
            

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Main page
@app.route('/')
def index():

    data = {'bottom_left_e' : [0],
                   'bottom_left_n' : [0],
                   'bottom_right_e' : [0],
                   'bottom_right_n' : [0],
                   'top_left_e' : [0],
                   'top_left_n' : [0],
                   'top_right_e' : [0],
                   'top_right_n' : [0],
                   'coord_system' : ["hiii"]}

    df = pd.DataFrame.from_dict(data)

    server = 'ec2-52-3-60-53.compute-1.amazonaws.com' 
    database = 'd3kr6lkene46qr' 
    username = 'mnonspcirnraqg' 
    password = '7919dd02f614cb83509e2889ec281800889dec45fb24c57db99d632e678f5626' 


    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{server}/{database}')
    con = engine.connect()
    df.to_sql('simulations', con=con, if_exists='append', index=False)
    con.close()
    
    #df1 = db.execute("SELECT * FROM Simulations")

    #printer()

    user = db.execute("SELECT * FROM simulations LIMIT 50")
    
    print(user)
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
    
    
    data = db.execute("SELECT * FROM simulations LIMIT 50")
    
    reporter()
    return render_template("loading.html", data=data)

@app.route("/report")
def report():
    return render_template("report.html")

if __name__ == "__main__":
    app.run()




