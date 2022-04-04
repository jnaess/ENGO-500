import re
import os
import io

import numpy as np

import base64

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
import matplotlib.pyplot as plt

from reports import reporter
from manager import Manager
from point import Coord

import time

app = Flask(__name__)

# Configure Database
#db = SQL("postgresql://mnonspcirnraqg:7919dd02f614cb83509e2889ec281800889dec45fb24c57db99d632e678f5626@ec2-52-3-60-53.compute-1.amazonaws.com:5432/d3kr6lkene46qr") 

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

    #manager = Manager()
    
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
    
    #insert simulation function here
    ####################
    data = db.execute("SELECT * FROM simulations LIMIT 50")
    
    #reporter()
    return render_template("loading.html", data=data)


# Rout to run the simulator
@app.route("/simulator", methods=['POST', 'GET'])
def simulator():
    
    return render_template("simulator.html")





@app.route("/report")
def report():    
    
    
    # Plot 1
    data = io.BytesIO()
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    plt.savefig(data, format='png', bbox_inches="tight")
    plt.close()
    encoded_img_data = base64.b64encode(data.getvalue())
    img = encoded_img_data.decode('UTF-8')
    
    # Plot 2
    data = io.BytesIO()
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some more numbers')
    plt.savefig(data, format='png')
    plt.close()
    encoded_img_data2 = base64.b64encode(data.getvalue())
    


    manager = Manager(mean_jump = Coord(0,0, std = [0, 0]),
                      jump_occurance_probability = 500,
                      easting_jump_const = 0,
                      northing_jump_const = .2)
    test = manager.plot_a()
    #im = Image.open("static/Images/Evan.png")
    

    return render_template("report.html", img_data=test, img_data2=encoded_img_data2.decode('UTF-8'))


if __name__ == "__main__":
    app.run()




