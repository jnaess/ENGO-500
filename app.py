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

from classes import *
from test_folder.test_script import printer

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Main page
@app.route('/')
def index():

    """goal_file = "scripts/Output_Tracks.csv"

    df = pd.read_csv(goal_file)

    df.columns
    std = [df['True_N_std'].to_list(),df['True_N_std'].to_list()]
    tru_N = df['True_N_std'].to_list()
    tru_E = df['True_E_std'].to_list()
    rename_keys = ["Unnamed: 0", "Real_E", "Real_N", "Real_E_std", "Real_N_std"]

    ED = ErrorDetector(df, tru_E, tru_N, rename_keys = rename_keys, true_std = std, is_static=False)

    ED.generate_error_dataframe()
    ED.drift_df.to_csv("scripts/test_analysis_drift.csv")
    ED.jump_df.to_csv("scripts/test_analysis_jump.csv")
    ED.errors_df.to_csv("scripts/test_analysis_errors.csv")"""
    
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




