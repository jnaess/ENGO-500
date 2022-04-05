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


# Route to run the simulator
@app.route("/simulator", methods=['POST', 'GET'])
def simulator():
    
    return render_template("simulator.html")





@app.route("/report",  methods=['POST', 'GET'])
def report():    
    
    width = float(request.form.get("width"))
    length = float(request.form.get("length"))
    swath = float(request.form.get("swath"))
    
    #render error or default max width
    if width * length > 640001:
        width = 800
        length = 800

    manager = Manager(field = [[0,0],[0,length],[width,length],[width,0]],
                                use_drift = True, 
                                 use_jump = True, 
                                 easting_drift_const = .01,
                                 northing_drift_const = .01,
                                 mean_jump = Coord(0,0,std = [.05, .05]),
                                 jump_occurance_probability = 500,
                                 drift_variability = Coord(0,0, std = [.001, .001]),
                                 easting_jump_const = .2,
                                 northing_jump_const = .2,
                                 tractor_speed = 1, 
                                 epoch_frequency = 1, 
                                 rename_keys = ["epoch", "real_e", "real_n", "real_e_std", "real_n_std"], 
                                 is_static = False, 
                                 true_std = [.1,.1],
                                tractor_width = swath)
    
    data = io.BytesIO()
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    plt.savefig(data, format='png', bbox_inches="tight")
    plt.close()
    encoded_img_data = base64.b64encode(data.getvalue())
    
    #test = manager.plot_a()
    test = encoded_img_data.decode('UTF-8')

    
    # Cost summary params
    seed = 0.016 # cost per m
    fert = 0.015 # cost per m
    herb = 0.012 # cost per m
    crop = 0.246 # profit per m
    net = 0.203 # net profit per m
    cost_params = [seed, fert, herb, crop, net]
    
    # Field area
    tot_area = width * length
    
    field_params = [width, length, tot_area, swath]
    
    # Maximum profit 
    tot_prof = net * tot_area
    
    # Peramters derived from over/underlap; true profit
    derived_params = [tot_prof * 0.60]
    
    
    # Area Coverage params; zero pass area, single pass area, double pass area
    area_params = [round(manager.zero_pass_area,3), 
                   round(manager.single_pass_area,3), 
                   round(manager.double_pass_area,3)]
    
    #losses; seed, fertilizer, harvest
    zero_pass_loss = [round(.203*manager.zero_pass_area,2),
                      round(.1258*manager.zero_pass_area,2),
                      round(.203*manager.zero_pass_area,2)]
    
    double_pass_loss = [round(.01637*manager.double_pass_area,2),
                        round(.026984**manager.double_pass_area,2),
                        0]
                      
    # Area coverage figures; all, zero pass, single pass, double pass
    area_plts = [manager.clean_track_plot, #track_summary_plot
                 manager.zero_pass_plot, 
                 manager.single_pass_plot, 
                 manager.double_pass_plot]
    
    # Error plots; detected track jumps, pass-to-pass accuracy, drift comaprison, 
    error_plts = [manager.sim_v_ED_cum_easting_drift_plot, 
                  manager.sim_v_ED_cum_northing_drift_plot, 
                 manager.sim_v_ED_cum_easting_jump_plot]
    
    # Simulator Cumulative df; #jumps, #drift, #errors, #cumjumpsE, #cumdriftE, #cumerrorsE,  #cumjumpsN, #cumdriftN, #cumerrorsN, 
    sim_df = manager.sim_detected + manager.sim_cum_count_e + manager.sim_cum_count_n
    
    # ED df; #jumps, #drift, #errors, #cumjumps, #cumdrift, #cumerrors, 
    ED_df = manager.ed_detected + manager.ed_cum_count_e + manager.ed_cum_count_n
    
    #Percent for ED; accjumps, accdrifts, accerrors, jumpsE, driftE, errorE, driftsN, jumpsN, errorN
    per_ED_df = manager.ed_detection_accuracy + manager.ed_cumulative_accuracy_e + manager.ed_cumulative_accuracy_n
    
    # Pass-to-Pass; simp2pE, simp2pN, EDp2pE, EDp2pN, ED%E, ED%N
    p2p = [round(manager.pass_to_pass_sim_e,4), 
           round(manager.pass_to_pass_sim_n,4), 
           round(manager.pass_to_pass_ed_e,4), 
           round(manager.pass_to_pass_ed_n,4), 
           manager.ed_pass_to_pass_accuracy[0], 
           manager.ed_pass_to_pass_accuracy[1]]
    
    return render_template("report.html", 
                           field_params=field_params, 
                           cost_params=cost_params, 
                           area_plts=area_plts, 
                           derived_params =derived_params, 
                           area_params=area_params, 
                           error_plts=error_plts, 
                           img_data2=test, 
                           sim_df=sim_df, 
                           ED_df=ED_df, 
                           per_ED_df=per_ED_df,
                           p2p=p2p,
                          zero_pass_loss = zero_pass_loss,
                          double_pass_loss = double_pass_loss)


# Route to run the simulator
@app.route("/classes")
def classes():
    
    
    return render_template("classes.html")


if __name__ == "__main__":
    app.run()




