from flask import Flask, redirect, render_template, request, session, jsonify
import requests
import pandas as pd
from shapely.geometry import Point
import pkg_resources
from geopandas import GeoDataFrame
import json

app=Flask(__name__)
@app.route('/')

def root():
    
    df = pd.DataFrame({#'zip':[19152,19047],
                   'Lat':[40.058841,40.202162],
                   'Lon':[-75.042164,-74.924594]})

    geometry = [Point(xy) for xy in zip(df.Lon, df.Lat)]

    gdf = GeoDataFrame(df, geometry=geometry)

    geoJSON = gdf.to_json()
    geoJSON = json.loads(geoJSON)

    return render_template('index.html',json_string = geoJSON)

if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)